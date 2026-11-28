"""Match remote review returns to local bytes using read-only OpenCode v2 calls."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


class Mismatch(ValueError):
    """A diagnostic safe to show without printing the host's response."""


def digest(path):
    if not path.is_file():
        raise Mismatch('artifact missing or not a regular file')
    sha = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            sha.update(chunk)
    return sha.hexdigest()


def api(operation, child, *params):
    cmd = ['opencode', 'api', operation, '--param', f'sessionID={child}']
    for param in params:
        cmd.extend(['--param', param])
    try:
        reply = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, check=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        raise Mismatch(f'OpenCode {operation} unavailable') from None
    try:
        return json.loads(reply.stdout)['data']
    except (ValueError, KeyError, TypeError):
        raise Mismatch(f'malformed OpenCode {operation} response') from None


def verify_return(role, child, parent, qualified, marker):
    session = api('session.get', child)
    if not isinstance(session, dict) or session.get('id') != child or session.get('parentID') != parent:
        raise Mismatch(f'{role}: child or parent mismatch')
    if role != 'design' and 'fork' in session:
        raise Mismatch(f'{role}: forked session is not a cold review')
    if 'outcome' in session and session['outcome'] != 'succeeded':
        raise Mismatch(f'{role}: session outcome not successful')
    agent = session.get('agent')
    if not isinstance(agent, str) or not agent.strip():
        raise Mismatch(f'{role}: missing session agent')

    # Do not filter to assistants: a newer user, tool step or failed idle invalidates an older return.
    messages = api('session.message.list', child, 'order=desc', 'limit=2')
    if not isinstance(messages, list) or len(messages) != 2 or not all(isinstance(m, dict) for m in messages):
        raise Mismatch(f'{role}: missing settled return')
    idle, answer = messages
    if idle.get('type') != 'idle' or idle.get('outcome') != 'succeeded' or 'error' in idle:
        raise Mismatch(f'{role}: latest turn not successfully idle')
    time = answer.get('time')
    if (answer.get('type') != 'assistant' or answer.get('finish') != 'stop' or 'error' in answer
            or not isinstance(time, dict) or type(time.get('completed')) not in (int, float)):
        raise Mismatch(f'{role}: missing completed assistant answer')
    if answer.get('agent') != agent:
        raise Mismatch(f'{role}: assistant agent mismatch')
    model = answer.get('model')
    if (not isinstance(model, dict) or ('variant' in model and not isinstance(model['variant'], str))
            or (model.get('providerID'), model.get('id'), model.get('variant')) not in qualified):
        raise Mismatch(f'{role}: assistant profile not qualified')

    parts = answer.get('content')
    if not isinstance(parts, list):
        raise Mismatch(f'{role}: malformed assistant content')
    text = []
    for part in parts:
        if not isinstance(part, dict):
            raise Mismatch(f'{role}: malformed assistant part')
        kind = part.get('type')
        if kind == 'tool':
            state = part.get('state')
            if not isinstance(state, dict) or state.get('status') != 'completed':
                raise Mismatch(f'{role}: unfinished or failed tool step')
            text.clear()  # Only the answer after the last tool can be a return.
        elif kind == 'text' and isinstance(part.get('text'), str):
            text.append(part['text'])
        elif kind != 'reasoning':
            raise Mismatch(f'{role}: malformed assistant part')
    lines = '\n'.join(text).splitlines()
    if not lines or lines[-1] != marker:
        raise Mismatch(f'{role}: final return marker mismatch')
    if not any(not line.lstrip().startswith('AI4SCI-REMOTE') and any(c.isalpha() for c in line)
               for line in lines[:-1]):
        raise Mismatch(f'{role}: missing review text before marker')
    return time['completed']


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('plan', type=Path)
    p.add_argument('package', type=Path)
    for name in ('parent', 'design', 'science', 'launch'):
        p.add_argument('--' + name, required=True)
    p.add_argument('--design-parent', help='original design parent for a resumed study')
    p.add_argument('--contributor', action='append', default=[], metavar='CHILD')
    p.add_argument('--qualified', action='append', required=True, metavar='PROVIDER/MODEL[#VARIANT]')
    args = p.parse_args(argv)
    try:
        qualified = []
        for profile in args.qualified:
            match = re.fullmatch(r'([^/#\s]+)/([^#\s]+)(?:#([^#\s]+))?', profile)
            if not match:
                raise Mismatch('malformed qualified profile')
            qualified.append(match.groups())
        children = (args.design, args.science, args.launch)
        design_parent = args.design_parent if args.design_parent is not None else args.parent
        parents = {args.parent, design_parent}
        if not all(re.fullmatch(r'ses[^\s]*', s) for s in (*children, *parents, *args.contributor)):
            raise Mismatch('malformed session ID')
        if len(set(children)) != 3 or parents.intersection(children):
            raise Mismatch('review child reused or also a parent')
        if set(args.contributor).intersection((args.science, args.launch)):
            raise Mismatch('final reviewer reused from contributors')
        plan, package = digest(args.plan), digest(args.package)
        design_time = verify_return('design', args.design, design_parent, qualified, f'AI4SCI-REMOTE design {plan}')
        pending = []
        for role, child in [('science', args.science), ('launch', args.launch)]:
            marker = f'AI4SCI-REMOTE {role} {plan} {package}'
            completed = verify_return(role, child, args.parent, qualified, marker)
            if not (completed >= design_time):
                pending.append(role)
        if pending:
            raise Mismatch('Latest design return: acknowledgement pending from ' + ', '.join(pending))
    except OSError:
        print('artifact unreadable', file=sys.stderr)
        return 1
    except Mismatch as e:
        print(e, file=sys.stderr)
        return 1
    print('Design, science and launch review return references matched.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
