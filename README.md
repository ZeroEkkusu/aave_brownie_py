# About
A Brownie suite for basic interaction with the [Aave protocol](https://github.com/aave/protocol-v2). Includes depositing, borrowing, repaying, and other functionality. Suitable for quantitative defi engineering, as well.
### Example
<p align="center">
<img src="https://raw.githubusercontent.com/ZeroEkkusu/aave_brownie_py/main/img/example.png" alt="Example integration test output">
</p>

### Todo
- [ ] Licences and credits
- [ ] CHALLENGE: short sell
- [ ] Repay the remaining debt with the collateral using flash loans
	- [ ] Change tests
# Setup
Clone this repo
```bash
git clone https://github.com/ZeroEkkusu/aave_brownie_py
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
