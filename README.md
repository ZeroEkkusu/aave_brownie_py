# About
A Brownie suite for basic interaction with the [Aave protocol](https://github.com/aave/protocol-v2). Includes depositing, borrowing, repaying, and other functionality.
Suitable for quantitative defi engineering, as well.
### Example

<br/>
<p align="center">
<img src="TODO" alt="Example integration test output">
</p>
<br/>

### Todo
- [ ] CHALLENGE: short sell
- [ ] Repay the remaining debt with the collateral using flash loans
	- [ ] Change tests
# Setup
Clone this repo
```bash
git clone this
```
### Prerequisites
- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)
### Requirements
```bash
pip install -r requirements.txt
```
### Other files
Set up your `.env` file using the provided `.env.example`
Or encrypt your private key:
```bash
brownie accounts new <choose_account_id>
```
# Usage
- Make sure you have excess DAI in your account before running the integration test - [Kovan DAI Faucet](https://staging.aave.com/#/faucet). *This will change after implementing the flash loan + swap functionality*
- Make sure the account is debt-free before testing - **IMPORTANT**
### Compile
```bash
brownie compile
```
### Test
```bash
brownie test --network <choose_network>
```