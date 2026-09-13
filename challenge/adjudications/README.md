# Public adjudication records

This directory is the public registry for completed substantive challenge adjudications.

The governing contract is `../ADJUDICATION-CONTRACT.md`. Public challenge receipt and
pending visibility are governed separately by `../LIFECYCLE-CONTRACT.md` and
`../receipts/`.

`index.json` lists immutable adjudication-record paths. An empty list means that no
completed public adjudication record is currently registered; pending public challenges
are visible through the receipt registry instead.

A later correction creates a new record that names the earlier adjudication in
`supersedes`. Earlier records are not silently deleted or rewritten.

The registry contains public governance material only. It is not a disclosure channel for
private implementation, CI, tests, red-team material, or private reference-opening
material.
