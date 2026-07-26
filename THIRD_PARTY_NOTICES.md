# Third-party notices — Generic Voice

This repository redistributes or depends on third-party components.
Generic Voice application code (Python modules under `py/` and `lib/` excluding
bundled engine binaries and voice models) is released under the MIT License
(see [LICENSE](LICENSE)).

## Runtime dependencies (Python)

| Package | License (typical) | Role |
|---------|-------------------|------|
| numpy | BSD | Audio arrays |
| scipy | BSD | Signal processing / WAV I/O |
| inquirer | MIT | Interactive prompts |
| edge-tts | MIT | Microsoft Edge cloud TTS client |
| flet / flet-web | Apache-2.0 | Optional GUI |

Install pins live in [requirements.txt](requirements.txt). Always verify the
license of the exact package version you install.

## Bundled / shipped components

### Piper TTS binaries and ONNX Core voices

- Location: `lib/tts/piper/`
- Piper is generally distributed under the **MIT** license by its upstream project.
- This repository ships selected Core voice archives (`*.zip.*`) for five languages
  and the Piper runtime binaries used on Linux.
- Upstream project: https://github.com/rhasspy/piper

### eSpeak NG data / helper binary

- Location: `lib/tts/piper/bin/espeak-ng*` and `espeak-ng-data/`
- eSpeak NG is licensed under **GPLv3**.
- Redistribution of these binaries/data with Generic Voice therefore carries
  GPLv3 obligations for those components. Source availability for eSpeak NG:
  https://github.com/espeak-ng/espeak-ng

### Edge TTS (online)

- No Microsoft binary is shipped.
- When `--tts edge` is used, text is sent to Microsoft’s online TTS service via
  the `edge-tts` client. That path is **not offline** and is subject to Microsoft’s
  terms and network availability.

### ONNX Runtime shared libraries

- Location: `lib/tts/piper/bin/libonnxruntime.so*`
- ONNX Runtime is typically MIT-licensed upstream:
  https://github.com/microsoft/onnxruntime

## Operator notes

1. Do not remove this file when redistributing binaries or voice archives.
2. If you strip GPLv3 components (eSpeak data/binary), document the change clearly.
3. Cloud synthesis (Edge) may transmit user text off-machine — disclose this in
   any product that wraps Generic Voice.
4. Pricing, commercial roadmaps, and internal packaging scripts are **not** part
   of this public tree.
