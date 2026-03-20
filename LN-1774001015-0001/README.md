# Loan LN-1774001015-0001

## Closing Transactions

This directory contains pre-signed closing transactions for loan LN-1774001015-0001.

| Outcome | File | Timelock | Output To |
|---------|------|----------|-----------|
| repayment | LN-1774001015-0001-repayment.hex | None | borrower |
| default | LN-1774001015-0001-default.hex | 2026-04-19T10:03:35.306107+00:00 | liquidator |
| liquidation | LN-1774001015-0001-liquidation.hex | None | liquidator |
| cancellation | LN-1774001015-0001-cancellation.hex | None | borrower |
| disaster | LN-1774001015-0001-disaster.hex | 2026-05-19T10:03:35.306107+00:00 | borrower |

## How to Use

If SATS.LEND server is down, you can still close your loan:

1. Download the appropriate .hex file
2. Go to https://blockstream.info/tx/push (mainnet) or https://blockstream.info/testnet/tx/push (testnet)
3. Paste the raw_hex value and broadcast

## Loan Details
- Amount: $100.0 USDC
- Collateral: 0.0028380750472184733 BTC
- Escrow: 359SYTiqE4g5ApoCT7tLdTgjZPXJem2xe2
- Maturity: 2026-04-19T10:03:35.306107+00:00
- BTC Price at Creation: $70470.3
- Network: MAINNET

## Disaster Recovery
If everything fails, use `LN-1774001015-0001-disaster.hex` after 2026-04-19T10:03:35.306107+00:00 + 30 days.
