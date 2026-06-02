import { Link } from 'react-router-dom';
import './Footer.scss';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer__inner container">
        <div className="footer__left">
          <span className="footer__logo">Quiz<span>Hub</span></span>
          <p className="footer__copy">© 2025 QuizHub. Всі права захищені.</p>
        </div>
        <div className="footer__links">
          <Link to="/quizzes">Тести</Link>
          <Link to="/register">Реєстрація</Link>
          <Link to="/login">Вхід</Link>
        </div>
      </div>
    </footer>
  );
}
