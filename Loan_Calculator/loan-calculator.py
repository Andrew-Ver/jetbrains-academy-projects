import math
import argparse

def parse_input() -> dict:
	parser = argparse.ArgumentParser()
	parser.add_argument('--type', type=str, required=True, help='either diff or annuity')
	parser.add_argument('--payment', type=float, help='monthly payment amount')
	parser.add_argument('--principal', type=float, help='principal loan amount')
	parser.add_argument('--periods', type=int, help='number of payment periods')
	parser.add_argument('--interest', type=float, help='annual interest amount')
	args = parser.parse_args()
	argument_dict = {arg: getattr(args, arg) for arg in vars(args)}
	if len([a for a in argument_dict if argument_dict[a]]) < 4 or (argument_dict['type'] == 'diff' and not argument_dict['interest']):
		print('Incorrect parameters')
		return False
	return {a: argument_dict[a] for a in ['type', 'payment', 'principal', 'periods', 'interest']}

class Calculator():
	def __init__(self, principal: float = 0, interest: float = 0, n_of_payments: int = 0, monthly_payment: float = 0) -> None:
		self.interest = interest/(12*100)
		self.principal = principal 
		self.n_of_payments = n_of_payments
		self.monthly_payment = monthly_payment

	def calc_payment_amount(self) -> float:
		return math.ceil(self.principal / ( (((1+self.interest)**self.n_of_payments)-1) / (self.interest * (1+self.interest)**self.n_of_payments )))

	def calc_number_of_payments(self) -> float:
		x = self.monthly_payment / (self.monthly_payment-self.interest*self.principal)
		base = 1+self.interest
		return math.ceil(math.log(x, base))

	def calc_loan_principal(self) -> float:
		divisor = (self.interest*(1+self.interest)**self.n_of_payments) / (((1+self.interest)**self.n_of_payments) -1)
		return self.monthly_payment / divisor

	def calc_differentiated_payment(self, month: int) -> float:
		return (self.principal/self.n_of_payments) + (self.interest) * (self.principal - (self.principal*(month-1)/self.n_of_payments))

	def display_answer(self, parameter: str) -> None:
		# Print the Answer
		if parameter == 'annuity':
			if self.principal and self.monthly_payment and self.interest:
				self.n_of_payments = self.calc_number_of_payments()
				yrs, mths = divmod(self.n_of_payments, 12)
				if yrs < 1:
					print(f'It wll take {mths} months to repay this loan!')
				elif yrs > 1 and not mths:
					print(f'It will take {yrs} years to repay this loan!')
				else:
					print(f'It will take {yrs} years and {mths} months to repay this loan!')
			elif self.principal and self.n_of_payments and self.interest:
				self.monthly_payment = self.calc_payment_amount()
				print(f'Your monthly payment = {self.monthly_payment}!')
			elif self.monthly_payment and self.n_of_payments and self.interest:
				self.principal = math.floor(self.calc_loan_principal())
				print(f'Your loan principal = {self.principal}!')
			overpayment = (self.n_of_payments * self.monthly_payment) - self.principal
		elif parameter == 'diff':
			monthly_payments = [math.ceil(self.calc_differentiated_payment(mth)) for mth in range(1, self.n_of_payments+1)]
			overpayment = sum(monthly_payments) - self.principal
			for m in range(1, self.n_of_payments+1):
				print(f'Month {m}: payment is: {monthly_payments[m-1]}')
		if overpayment > 0:
				print(f'Overpayment = {int(overpayment)}')

parsed_input = parse_input()
if parsed_input:
	calc = Calculator(principal=parsed_input['principal'], interest=parsed_input['interest'], n_of_payments=parsed_input['periods'], monthly_payment=parsed_input['payment'])
	calc.display_answer(parsed_input['type'])
else:
	print(f'Exitting...')