# Loan LN-1773767580-0001

## Closing Transactions

This directory contains pre-signed closing transactions for loan LN-1773767580-0001.

| Outcome | File | Timelock | Output To |
|---------|------|----------|-----------|
| repayment | LN-1773767580-0001-repayment.hex | None | borrower |
| default | LN-1773767580-0001-default.hex | 2026-04-16T17:13:00.288532+00:00 | liquidator |
| liquidation | LN-1773767580-0001-liquidation.hex | None | liquidator |
| cancellation | LN-1773767580-0001-cancellation.hex | None | borrower |
| disaster | LN-1773767580-0001-disaster.hex | 2026-05-16T17:13:00.288532+00:00 | borrower |

## How to Use

If SATS.LEND server is down, you can still close your loan:

1. Download the appropriate .hex file
2. Go to https://blockstream.info/tx/push (mainnet) or https://blockstream.info/testnet/tx/push (testnet)
3. Paste the raw_hex value and broadcast

## Loan Details
- Amount: $100.0 USDC
- Collateral: 0.0026959144629475538 BTC
- Escrow: 3EZ8mf2pGFkUoVKkGD7ZPSqT3Ckk4uvV6D
- Maturity: 2026-04-16T17:13:00.288532+00:00
- BTC Price at Creation: $74186.33
- Network: MAINNET

## Disaster Recovery
If everything fails, use `LN-1773767580-0001-disaster.hex` after 2026-04-16T17:13:00.288532+00:00 + 30 days.
