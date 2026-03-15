# Loan LN-TEST-001

## Closing Transactions

This directory contains pre-signed closing transactions for loan LN-TEST-001.

| Outcome | File | Timelock | Output To |
|---------|------|----------|-----------|
| repayment | LN-TEST-001-repayment.hex | None | borrower |
| default | LN-TEST-001-default.hex | 2026-04-15T00:00:00+00:00 | lender |
| disaster | LN-TEST-001-disaster.hex | 2026-05-15T00:00:00+00:00 | borrower |

## How to Use

If SATS.LEND server is down, you can still close your loan:

1. Download the appropriate .hex file
2. Go to https://blockstream.info/tx/push (mainnet) or https://blockstream.info/testnet/tx/push (testnet)
3. Paste the raw_hex value and broadcast

## Loan Details
- Amount: $100 USDC
- Collateral: 0.003 BTC
- Escrow: 3TestAddress
- Maturity: 2026-04-15T00:00:00+00:00
- BTC Price at Creation: $71000
- Network: MAINNET

## Disaster Recovery
If everything fails, use `LN-TEST-001-disaster.hex` after 2026-04-15T00:00:00+00:00 + 30 days.
