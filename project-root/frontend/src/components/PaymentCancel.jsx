import { Link } from 'react-router-dom'

function PaymentCancel() {
  return (
    <div>
      <h2>Payment Canceled</h2>
      <p>Your purchase was not completed. No charge has been made.</p>
      <p><Link to="/">Return to App</Link></p>
    </div>
  )
}

export default PaymentCancel
