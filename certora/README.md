# SILO V2 Formal Verification Contest Repo

This repo was submitted by me (BenRai1) for the [Silo V2 Audit + Certora Formal Verification competition](https://cantina.xyz/competitions/18f1e37b-9ac2-4ba9-b32e-50344500c1a7/leaderboard) on Cantina running from the 13th of January 2025 to 10th of February 2025.

The goal of the formal verification part of the competition was to formally verify the following contracts using the Certora Prover:

| Contract                                                                                                                                                      | SLOC |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| [Silo.sol](https://github.com/BenRai1/silo-v2-cantina-fv/blob/main/silo-core/contracts/Silo.sol)                                                              | 452  |
| [PartialLiquidation.sol](https://github.com/BenRai1/silo-v2-cantina-fv/blob/main/silo-core/contracts/utils/hook-receivers/liquidation/PartialLiquidation.sol) | 155  |
| [Actions.sol](https://github.com/BenRai1/silo-v2-cantina-fv/blob/main/silo-core/contracts/lib/Actions.soll)                                                   | 373  |

I wrote a total of [325 rules](https://github.com/BenRai1/silo-v2-cantina-fv/tree/main/certora/specs) and managed to catch 18 out of 28 mutations used for [evaluating the submissions](https://docs.google.com/spreadsheets/d/1libTv86GVO0MKF9gl-4PRoVXPtp_6xEmss0HT0ZNIdo/edit?gid=1970712821#gid=1970712821) which place me 3rd in the FV contest.