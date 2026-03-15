# Loan LN-1773577697-0001

## Closing Transactions

This directory contains pre-signed closing transactions for loan LN-1773577697-0001.

| Outcome | File | Timelock | Output To |
|---------|------|----------|-----------|
| repayment | LN-1773577697-0001-repayment.hex | None | borrower |
| default | LN-1773577697-0001-default.hex | 2026-04-14T12:28:17.448951+00:00 | liquidator |
| liquidation | LN-1773577697-0001-liquidation.hex | None | liquidator |
| cancellation | LN-1773577697-0001-cancellation.hex | None | borrower |
| disaster | LN-1773577697-0001-disaster.hex | 2026-05-14T12:28:17.448951+00:00 | borrower |

## How to Use

If SATS.LEND server is down, you can still close your loan:

1. Download the appropriate .hex file
2. Go to https://blockstream.info/tx/push (mainnet) or https://blockstream.info/testnet/tx/push (testnet)
3. Paste the raw_hex value and broadcast

## Loan Details
- Amount: $100.0 USDC
- Collateral: 0.002788784568204816 BTC
- Escrow: 39qWSJ1oS2z7N8GzWEoH2qU6S2PPNH5pPL
- Maturity: 2026-04-14T12:28:17.448951+00:00
- BTC Price at Creation: $71715.83
- Network: MAINNET

## Disaster Recovery
If everything fails, use `LN-1773577697-0001-disaster.hex` after 2026-04-14T12:28:17.448951+00:00 + 30 days.
