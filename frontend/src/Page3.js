import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
const API_URL = process.env.REACT_APP_API_URL;

function Page3() {
  const location = useLocation();
  const navigate = useNavigate();
  const params = new URLSearchParams(location.search);

  const [filter, setFilter] = useState({
    date: params.get('date') || '',
    first_name: params.get('first_name') || '',
    last_name: params.get('last_name') || '',
  });
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState({ items: [], total: 0 });
  const [uniqueNames, setUniqueNames] = useState({ first: [], last: [] });

  useEffect(() => {
    // Fetch unique names (assuming we get all history without filters first for selects)
    const fetchUniques = async () => {
      try {
        const today = new Date().toISOString().split('T')[0];
        const response = await fetch(`${API_URL}/api/history?date=${today}`);
        const history = await response.json();
        const firstSet = new Set(history.items.map(item => item.first_name));
        const lastSet = new Set(history.items.map(item => item.last_name));
        setUniqueNames({ first: Array.from(firstSet), last: Array.from(lastSet) });
      } catch {}
    };
    fetchUniques();

    if (filter.date) {
      handleShow();
    }
  }, []);

  const handleChange = (e) => {
    setFilter({ ...filter, [e.target.name]: e.target.value });
  };

  const handleShow = async () => {
    if (!filter.date) return;
    setLoading(true);
    try {
      const query = new URLSearchParams({
        date: filter.date,
        ...(filter.first_name && { first_name: filter.first_name }),
        ...(filter.last_name && { last_name: filter.last_name }),
      }).toString();
      const response = await fetch(`${API_URL}/api/history?${query}`);
      const result = await response.json();
      setData(result);
      navigate(`/history?${query}`, { replace: true });
    } catch {}
    setLoading(false);
  };

  return (
    <div>
      <h1>History</h1>
      <form className="filter">
        <input type="date" name="date" value={filter.date} onChange={handleChange} required />
        <select name="first_name" value={filter.first_name} onChange={handleChange}>
          <option value="">Select First Name</option>
          {uniqueNames.first.map(name => <option key={name} value={name}>{name}</option>)}
        </select>
        <select name="last_name" value={filter.last_name} onChange={handleChange}>
          <option value="">Select Last Name</option>
          {uniqueNames.last.map(name => <option key={name} value={name}>{name}</option>)}
        </select>
        <button type="button" onClick={handleShow}>Show</button>
				<div className="allocate-spinner">
      		{loading && <div className="spinner"></div>}
      	</div>
      </form>
      <table>
        <thead>
          <tr><th>Date</th><th>First Name</th><th>Last Name</th><th>Count</th></tr>
        </thead>
        <tbody>
          {data.items.map((item, idx) => (
            <tr key={idx}>
              <td>{item.date}</td>
              <td>{item.first_name}</td>
              <td>{item.last_name}</td>
              <td>{item.count}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <p>Total records: {data.total}</p>
    </div>
  );
}

export default Page3;
