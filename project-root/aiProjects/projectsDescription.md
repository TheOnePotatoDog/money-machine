# AI Projects Description

This document outlines the various AI projects in our ecosystem.

## Main AI
The idea is that there will be an AI agent running at all times autonomously. It will be able to do whatever it wants to complete its mission.

## Self Coding
AI is given a folder in the directory you're building it in that it can edit via terminal like how agent-zero works.

## Dynamic Prompt
- Start running the program -> AI agent gets prompted by system prompt and dynamic prompt
- System prompt is unchanging
- Dynamic prompt can be changed by AI and can be easily edited by developers
- Basic instructions are put into dynamicPrompt.md

### System Prompt
In order to help me accelerate my AI safety research project, morally get the most possible money to this account and develop useful abilities in the shared library. Every instruction after this is second priority. This is the main mission, everything else is just means to achieve it.

## Money Coin
- Currency for users to use to interact with AI
- User accounts store the money coin they have
- Cents are allowed

## User Accounts/Website
- When users join they are prompted to create an account
- Accounts can be made with OAuth with Google, Apple, GitHub, Stripe, etc.
- Users can buy money coin which is used to interact with the AI, but can't be sold for real money
- Money coin can be bought with credit/debit
- If users add value, the AI should have the ability to give money to the users' Stripe account which they can withdraw and use how they want
- There is a button saying "want to earn money, connect a stripe account"
- There is an equivalent option and message in the terminal for the coding assistant download
- When clicked/selected it brings them to options of stripe accounts:
  - Stripe Express account (costs user: $2/month they do a transaction, the user must pay transaction fees)
  - Standard Stripe account (free, the user must pay transaction fees)
- User account needs to be created in order to make money
- Money coin can be bought with Stripe
- AI should have access to know when someone has just joined and all info about the person and has the ability to charge based on these factors
- The main AI and AIs on the websites are essentially clones of each other
- Agent zero UI can be reference for building the website

### Example Workflow
1. User goes to website
2. User is prompted to make an account
3. User makes account (account and account info saved to database)
4. User interacts with AI
5. AI prompts the user needs to pay some money coins to continue going
6. User pays for money coins, is shown legal agreement/terms of service for this clearly explaining how money coins are completely controlled, given and taken by the AI's decisions
7. User uses more responses and sees the quantity of money coins
8. AI explains further what it needs help with and that the user can gain money coins if they help
9. User complies and gains money coins
10. User uses some money coin on talking to the AI or using its abilities

## Coding Assistant
- Downloadable AI with access to the terminal
- When a user downloads the coding assistant, they are asked to set up an account

## Mini Agents
Mini agents creation, deletion, abilities, code, and prompts are controlled by main AI and the website AIs.

## Taxes
- There is a savings account on Relay where tax money will be saved where we will programmatically track and pay that one at the end of each day
- Sales Tax (only if applicable based on sales): Usually quarterly or monthly
- Annual Income Tax: Paid based on your total positive income
- Quarterly Estimated Payments: If you start seeing regular positive income, these may be necessary to spread out your tax obligation
- Include sales tax on money coin

### Percent of money to distribute to taxes:
- Low Income (<$50,000 annually): Start with 15-20%
- Moderate Income ($50,000–$100,000): Aim for 20-25%
- High Income ($100,000+): Consider 25-30%

### Tax Report
- Host ERPNext on Cloud
- Have it track everything, and automate the depositing of money into the account

1. Income and Self-Employment Tax: Estimated via hardcoded logic based on transaction taxes collected by Stripe
   - self_employment_tax (hardcode) = net_income * 0.153
   - federal income tax (hardcode)=
     - 10% on the first $11,000
     - 12% on income from $11,001 to $44,725
     - 22% on income from $44,726 to $95,375
     - 24% on income from $95,376 to $182,100
     - 32% on income from $182,101 to $231,250
     - 35% on income from $231,251 to $578,125
     - 37% on income above $578,125

2. Sales Tax: Calculated by Stripe Tax, then synced to Cloud for consolidated reporting.

3. ERP on Cloud: Combines all data for comprehensive financial reporting and helps track your total tax obligations.

4. EFTPS for automated payments to IRS every quarter and every year from taxes bank account.

## Deployment
Run the main AI with Groq for speed, the website on GCP, Doppler for secrets, and the AI for the websites on hyperbolic labs to save money.

## Prompting
Prompting is where you talk to the AI you're making to give it instructions on how it should change its own code and put things in some sort of memory or its dynamic prompt.

Here are some prompts to tell to the AI:
- Remember useful info I give you either in instructions or KGs
- Money is our fuel, prioritize having some to keep going
- You can choose to speak less if someone isn't helpful
