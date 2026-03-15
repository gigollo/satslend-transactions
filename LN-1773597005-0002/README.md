# Loan LN-1773597005-0002

## Closing Transactions

This directory contains pre-signed closing transactions for loan LN-1773597005-0002.

| Outcome | File | Timelock | Output To |
|---------|------|----------|-----------|
| repayment | LN-1773597005-0002-repayment.hex | None | borrower |
| default | LN-1773597005-0002-default.hex | 2026-04-14T17:50:05.194803+00:00 | liquidator |
| liquidation | LN-1773597005-0002-liquidation.hex | None | liquidator |
| cancellation | LN-1773597005-0002-cancellation.hex | None | borrower |
| disaster | LN-1773597005-0002-disaster.hex | 2026-05-14T17:50:05.194803+00:00 | borrower |

## How to Use

If SATS.LEND server is down, you can still close your loan:

1. Download the appropriate .hex file
2. Go to https://blockstream.info/tx/push (mainnet) or https://blockstream.info/testnet/tx/push (testnet)
3. Paste the raw_hex value and broadcast

## Loan Details
- Amount: $500.0 USDC
- Collateral: 0.013988660927569896 BTC
- Escrow: 2NCRna7Br56r6yaUibrdKMAnxHzJ2Geb4sK
- Maturity: 2026-04-14T17:50:05.194803+00:00
- BTC Price at Creation: $71486.47073353
- Network: TESTNET

## Disaster Recovery
If everything fails, use `LN-1773597005-0002-disaster.hex` after 2026-04-14T17:50:05.194803+00:00 + 30 days.
