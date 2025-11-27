import { Link } from 'react-router-dom';

function Page1() {
  return (
    <div>
      <h1>Home Page 1</h1>
      <Link to="/submit">Go to Page 2</Link><br />
      <Link to="/history">Go to Page 3</Link>
    </div>
  );
}

export default Page1;
