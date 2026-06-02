import { Link } from 'react-router-dom';
import './NotFound.scss';

export default function NotFound() {
  return (
    <div className="not-found">
      <div className="not-found__inner">
        <div className="not-found__code">404</div>
        <h1>Сторінку не знайдено</h1>
        <p>Здається, ця сторінка зникла або ніколи не існувала</p>
        <div className="not-found__actions">
          <Link to="/" className="btn btn--primary">На головну</Link>
          <Link to="/quizzes" className="btn btn--outline">Переглянути тести</Link>
        </div>
      </div>
    </div>
  );
}
