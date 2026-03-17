# Loan LN-1773767527-0001

## Closing Transactions

This directory contains pre-signed closing transactions for loan LN-1773767527-0001.

| Outcome | File | Timelock | Output To |
|---------|------|----------|-----------|
| repayment | LN-1773767527-0001-repayment.hex | None | borrower |
| default | LN-1773767527-0001-default.hex | 2026-04-16T17:12:07.770282+00:00 | liquidator |
| liquidation | LN-1773767527-0001-liquidation.hex | None | liquidator |
| cancellation | LN-1773767527-0001-cancellation.hex | None | borrower |
| disaster | LN-1773767527-0001-disaster.hex | 2026-05-16T17:12:07.770282+00:00 | borrower |

## How to Use

If SATS.LEND server is down, you can still close your loan:

1. Download the appropriate .hex file
2. Go to https://blockstream.info/tx/push (mainnet) or https://blockstream.info/testnet/tx/push (testnet)
3. Paste the raw_hex value and broadcast

## Loan Details
- Amount: $100.0 USDC
- Collateral: 0.002695707342149824 BTC
- Escrow: 3QUbE8tAix8JpU2CgMAW62UgEWWBDp98np
- Maturity: 2026-04-16T17:12:07.770282+00:00
- BTC Price at Creation: $74192.03
- Network: MAINNET

## Disaster Recovery
If everything fails, use `LN-1773767527-0001-disaster.hex` after 2026-04-16T17:12:07.770282+00:00 + 30 days.
