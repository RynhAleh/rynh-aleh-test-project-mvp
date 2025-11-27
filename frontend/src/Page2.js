import { useState } from 'react';
import { Link } from 'react-router-dom';
const API_URL = process.env.REACT_APP_API_URL;

function Page2() {
  const [formData, setFormData] = useState({ date: '', first_name: '', last_name: '' });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});
    setSuccess(false);

    try {
      const response = await fetch(`${API_URL}/api/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) {
        setErrors(data.error || {});
      } else if (data.success) {
        setSuccess(true);
      }
    } catch (err) {
      setErrors({ general: ['Server error'] });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Submit Form</h1>
      <form onSubmit={handleSubmit}>
        <input type="date" name="date" value={formData.date} onChange={handleChange} required />
        <div className="allocate-err" />
        <input type="text" name="first_name" value={formData.first_name} onChange={handleChange} required placeholder="First Name" />
        <div className="allocate-err">{errors.first_name && <p className="error">{errors.first_name[0]}</p>}</div>
        <input type="text" name="last_name" value={formData.last_name} onChange={handleChange} required placeholder="Last Name" />
        <div className="allocate-err">{errors.last_name && <p className="error">{errors.last_name[0]}</p>}</div>
				<div className="allocate-spinner">
      		{loading && <div className="spinner"></div>}
      	</div>
        <button type="submit">Submit</button>
      </form>
      {success && (
        <div className="success">
          Data saved successfully! <Link to="/history">Go to Page 3</Link>
        </div>
      )}
      {errors.general && <p className="error">{errors.general[0]}</p>}
    </div>
  );
}

export default Page2;
