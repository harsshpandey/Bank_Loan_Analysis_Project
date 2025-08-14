-- A. Bank Loan Report | Summary
-- KPI's :

-- Total Loan Applications
Select count(id) As Total_Applications from bank_loan_data ;

-- MTD(Month to data) Loan Applications 
Select count(id) as Total_Applications from bank_loan_data
where MONTH(issue_date)= 12 ;

-- PMTD Loan Applications
Select count(id) as Total_Applications from bank_loan_data
where MONTH(issue_date) = 11 ;

-- -----------------------------------------------------------------------------

-- Total Funded Amount
Select Sum(loan_amount) as Total_Funded_Amount from bank_loan_data ;

-- MTD Total Amount
Select Sum(loan_amount) as Total_Funded_Amount from bank_loan_data 
where MONTH(issue_date) = 12 ;

-- PMTD Total Amount
Select Sum(loan_amount) as Total_Funded_Amount from bank_loan_data 
where MONTH(issue_date) = 11 ;

-- --------------------------------------------------------------------------
-- Total Amount Recieved 
Select Sum(total_payment) as Total_Amount_Collected from bank_loan_data ;

-- MTD Total Amount Recieved
Select Sum(total_payment) as Total_Amount_Collected from bank_loan_data
Where Month(issue_date) = 12 ;

-- PMTD Total Amount Recieved
Select Sum(total_payment) as Total_Amount_Collected from bank_loan_data
Where Month(issue_date) = 11 ;

-- -----------------------------------------------------------------------
-- Debt-to-Income Ratio 

-- AVG Interest Rate
Select Avg(int_rate) as Avg_Int_Rate From bank_loan_data;

-- MTD AVG Interest Rate
Select Avg(int_rate) as Avg_Int_Rate From bank_loan_data
Where MONTH(issue_date) = 12;

-- PMTD Interest Rate
Select Avg(int_rate) as Avg_Int_Rate From bank_loan_data
Where MONTH(issue_date) = 11;
-- ------------------------------------------------------------------------

-- Avg DTI
SELECT AVG(dti)*100 AS Avg_DTI FROM bank_loan_data ;

-- MTD Avg DTI
SELECT AVG(dti)*100 AS MTD_Avg_DTI FROM bank_loan_data
WHERE MONTH(issue_date) = 12 ;

-- PMTD Avg DTI
SELECT AVG(dti)*100 AS PMTD_Avg_DTI FROM bank_loan_data
WHERE MONTH(issue_date) = 11 ;

-- ------------------------------------------------------------------------

-- GOOD LOAN ISSUED

-- Good Loan Percentage
Select 
	(count(case when loan_status = 'Fully Paid' or loan_status = 'Current' then id
END )*100) /
	count(id) as Good_loan_Percentage
from bank_loan_data;

-- Good Loan Applications
Select 
	count(id) as bank_loan_data
from bank_loan_data
Where loan_status = 'Fully Paid' or loan_status = 'Current';

-- Good Loan Funded Amount
Select Sum(loan_amount)
from bank_loan_data
where loan_status = 'Fully Paid' or loan_status = 'Current';

-- Good Loan Amount Received
Select Sum(total_payment)
from bank_loan_data
where loan_status = 'Fully Paid' or loan_status = 'Current';

-- ---------------------------------------------------------------------
-- BAD LOAN ISSUED

-- Bad Loan Percentage
SELECT
    (COUNT(CASE WHEN loan_status = 'Charged Off' THEN id END) * 100.0) / 
	COUNT(id) AS Bad_Loan_Percentage
FROM bank_loan_data ;

-- Bad Loan Applications
SELECT COUNT(id) AS Bad_Loan_Applications FROM bank_loan_data
WHERE loan_status = 'Charged Off' ;

-- Bad Loan Funded Amount
SELECT SUM(loan_amount) AS Bad_Loan_Funded_amount FROM bank_loan_data
WHERE loan_status = 'Charged Off' ;

-- Bad Loan Amount Received
SELECT SUM(total_payment) AS Bad_Loan_amount_received FROM bank_loan_data
WHERE loan_status = 'Charged Off';


-- ----------------------------------------------------------------------------
-- LOAN STATUS
Select loan_status,
	count(id) as Loan_count,
	Sum(total_payment) as Total_amount_received,
	Sum(loan_amount) as Total_amount_Funded,
	Avg(int_rate *100) as Interest_rate,
	Avg(dti*100) as DTI
FROM bank_loan_data 
group by loan_status ;


SELECT 
	loan_status, 
	SUM(total_payment) AS MTD_Total_Amount_Received, 
	SUM(loan_amount) AS MTD_Total_Funded_Amount 
FROM bank_loan_data
WHERE MONTH(issue_date) = 12 
GROUP BY loan_status;


-- ----------------------------------------------------------------------------------

-- B. BANK LOAN REPORT | OVERVIEW

-- Month
SELECT 
    MONTH(issue_date) AS Month_Number, 
    MONTHNAME(issue_date) AS Month_Name, 
    COUNT(id) AS Total_Loan_Applications,
    SUM(loan_amount) AS Total_Funded_Amount,
    SUM(total_payment) AS Total_Amount_Received
FROM bank_loan_data
GROUP BY MONTH(issue_date), MONTHNAME(issue_date)
ORDER BY MONTH(issue_date);


-- STATE
SELECT 
	address_state AS State, 
	COUNT(id) AS Total_Loan_Applications,
	SUM(loan_amount) AS Total_Funded_Amount,
	SUM(total_payment) AS Total_Amount_Received
FROM bank_loan_data
GROUP BY address_state
ORDER BY address_state ;

-- TERM
SELECT 
	term AS Term, 
	COUNT(id) AS Total_Loan_Applications,
	SUM(loan_amount) AS Total_Funded_Amount,
	SUM(total_payment) AS Total_Amount_Received
FROM bank_loan_data
GROUP BY term
ORDER BY term ;


-- EMPLOYEE LENGTH
SELECT 
	emp_length AS Employee_Length, 
	COUNT(id) AS Total_Loan_Applications,
	SUM(loan_amount) AS Total_Funded_Amount,
	SUM(total_payment) AS Total_Amount_Received
FROM bank_loan_data
GROUP BY emp_length
ORDER BY emp_length ;

-- PURPOSE
SELECT 
	purpose AS PURPOSE, 
	COUNT(id) AS Total_Loan_Applications,
	SUM(loan_amount) AS Total_Funded_Amount,
	SUM(total_payment) AS Total_Amount_Received
FROM bank_loan_data
GROUP BY purpose
ORDER BY purpose ;


-- HOME OWNERSHIP
SELECT 
	home_ownership AS Home_Ownership, 
	COUNT(id) AS Total_Loan_Applications,
	SUM(loan_amount) AS Total_Funded_Amount,
	SUM(total_payment) AS Total_Amount_Received
FROM bank_loan_data
GROUP BY home_ownership
ORDER BY home_ownership ;



 





