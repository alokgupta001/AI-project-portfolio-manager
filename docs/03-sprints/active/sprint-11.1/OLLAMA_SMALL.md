# Small local Ollama setup

**Subsequent user decision:** Ollama's tray/server are now stopped and cloud work
continues with [Groq, Gemini and Puter](CLOUD_SPECIALISTS.md). Installed weights and
the launcher below remain preserved history. Do not restart local models as part
of the current cloud acceptance work. No additional local generation occurred.

17 October 2026. The user explicitly approved the proposed small-model trial, lifting
the earlier local-testing deferral for this controlled experiment. Installed
`qwen3:0.6b` and a native chat preset named **ppm-small**. The project remained running
throughout; no Docker/WSL restart, normal migration or cloud call occurred.

## Use the installed preset

Open PowerShell and run:

```powershell
& 'C:\Users\alokg\OneDrive\Documents\Codex\enterprise-ppm\scripts\start-ollama-small.ps1'
```

The [launcher](../../../../scripts/start-ollama-small.ps1) checks at least 3.5 GiB of
host RAM is available, pins the local loopback server, disables thinking for the
request, and requests immediate unloading after each response. Type `/bye` to leave
the interactive chat. The [Modelfile](../../../../config/ollama-small.Modelfile) sets
2,048 context tokens, 512 maximum generated tokens and temperature zero. Its creation
reused existing weights; it did not load another model or duplicate the weight file.
The thinking/unload controls belong to the launcher/API request, not the Modelfile;
opening the preset through another client does not inherit those two controls.

This is experimental native chat, separate from the project's supervised runtime.
The launcher performs an initial memory check; it does not impose the benchmark's
continuous RAM sampler or 22-second request deadline on interactive conversations.
The controlled tests below used both. It does not activate an application AI profile.

## Observed results

Fresh available host RAM was 4,319 MiB during installation, versus the earlier
1,261 MiB reading. These are changing observations, not a promise of future free RAM.
The trial therefore ran alongside the full normal stack without stopping services.

| Check | Observed result | Receipt |
| --- | --- | --- |
| Installed base | Qwen3 0.6B tag, GGUF Q4_K_M, 522,653,767 bytes; digest `7df6b6e09427a769808717c0a93cadc4ae99ed4eb8bf5ca557c90846becea435` | [installation](../../../verification/sprint11_1/implementation/qwen06-installation.json) |
| Base fixed-fact control | Passed at 2,048 context/128 output cap; 3.809 s including load, 22 generated tokens, minimum host available 3,475 MiB, zero models resident afterward | [control](../../../verification/sprint11_1/implementation/qwen06-small-context.json) |
| Actual project risk format | Complete transport in 3.568 s; rejected by unchanged SectionOutput consistency rules | [first attempt](../../../verification/sprint11_1/implementation/qwen06-risk-first.json) |
| Existing one-item replacement | Second and final attempt for that same calibration root: complete transport in 3.611 s, again INVALID_OUTPUT | [replacement](../../../verification/sprint11_1/implementation/qwen06-risk-repair.json) |
| Configured native preset | Fixed-fact control passed in 1.958 s at 2,048 context; sampled server + runner peak 890 MiB, minimum host available 3,468 MiB, zero resident models afterward | [preset control](../../../verification/sprint11_1/implementation/qwen06-alias-control.json) |
| Final operator regression | 53 offline tests passed, 1.82 s; actual memory descendant accounting, immediate unload, cold/warm classification and review gates | [tests](../../../verification/sprint11_1/implementation/qwen06-final-units.txt) |

Exactly **four local inference requests**: two fixed-fact setup controls and two
attempts for the same project-risk calibration case. No held-out case was consumed,
no unknown outcome occurred, and neither ledger nor the exhausted two-attempt risk
root was reset. The native preset was not used to rerun that exhausted risk case.
No successful project semantic qualification is claimed.

The project attempts emitted `no_findings` with an `unprocessed` gap and no covered
evidence, an inconsistent result rejected by the hard gate. Basic JSON transport
success does not establish useful project reasoning. The small candidate therefore
remains disabled/benchmark-only with no qualified task classes; all other profiles
and saved credentials remain unchanged.

## Memory evidence and limits

The first fixed-fact receipt's **88 MiB process peak counts only the server**, because
the old sampler selected fixed executable names and missed differently named runner
children. It is not a valid model-memory peak. That receipt's host-RAM samples and
latency remain valid. The corrected sampler follows process ancestry and includes
runner descendants while excluding unrelated processes. Later project peaks were
1,138/1,137 MiB, with minimum host available 3,240/3,215 MiB. All measured headroom
remained above the unchanged 2,048 MiB floor.

The small candidate's initial 1,024 MiB reservation was raised after measurement to
**1,536 MiB**, rounding measured peak +25% upward. Its resulting admission minimum
is 3,584 MiB available. This is a new model-specific reservation; the existing 4B
reservation/6 GiB start gate is unchanged. Working-set peaks are sampled sums and can
include shared pages; no exclusive footprint or instantaneous-peak claim is made.
See [setup record](../../../verification/sprint11_1/implementation/qwen06-setup.json).

The benchmark now supports `--keep-alive 0` or its existing default 60 seconds. Zero
residency rejects warm-repeat requests; cold loads are re-observed and must reserve
model memory each time. The scorer excludes cold timing samples from warm statistics.
Independent labels, broad per-class accuracy and representative warm/cold hardware
qualification are still required. This setup does not qualify the 4B model or all
nine specialist roles.

Native configuration follows [Ollama's Modelfile reference](https://docs.ollama.com/modelfile)
and [chat API controls](https://docs.ollama.com/api/chat). Download size is recorded from
the actual installed inventory, rather than used as a RAM estimate.

[Final closeout](../../../verification/sprint11_1/implementation/qwen06-closeout.json)
verifies 57 source/config/test fingerprints, 24 frozen files, five disabled profiles,
unchanged original profile/credential bindings, four completed local calls, preserved
two-attempt risk root and original three Groq admissions. Final resident-model count
is zero, normal revision remains 0012 and normal readiness returns HTTP 200.
