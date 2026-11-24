# A stronger baseline for predicting penguin body mass

A reviewer asked whether flipper length still helped when the constant predictor used the training median instead of the mean. On the same 119 held-out records, the reduction in mean absolute error fell from 384.7 g to 372.4 g. Read the [reply](research/response.md) and the [revised Word manuscript](paper/final.docx) for the comparison and its limits.

To check the study from the workflow checkout:

```sh
python3 ai4sci.py audit examples/penguins-revision/original
python3 ai4sci.py audit --submission examples/penguins-revision
(cd examples/penguins-revision && python3 replay.py && sha256sum --check original.sha256 artifacts.sha256 archive-completion.sha256)
```

The [original inventory](original.sha256) identifies the 13 files used to freeze the supplement. The [claim ledger](original/research/claims.json) and [source index](original/research/sources.json) were later copied byte-for-byte from the [previously published study](https://github.com/KomeijiReimu/ai4sci-workflow/tree/1c5d24060e1a1a67b551b1724427db3f77fefcb8/examples/penguins/research) so the archived manuscript can also be checked on its own. Their [separate checksums](archive-completion.sha256) leave the original inventory, plan and reviewed Word file unchanged.
