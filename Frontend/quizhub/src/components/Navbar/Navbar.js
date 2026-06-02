import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../../context/ThemeContext';
import './Navbar.scss';

export default function Navbar() {
  const { theme, toggle } = useTheme();
  const { pathname } = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  const links = [
    { to: '/', label: 'Головна' },
    { to: '/quizzes', label: 'Тести' },
    { to: '/leaderboard', label: 'Рейтинг' },
  ];

  return (
    <nav className="navbar">
      <div className="navbar__inner container">
        <Link to="/" className="navbar__logo">
          Quiz<span>Hub</span>
        </Link>

        <div className={`navbar__links ${menuOpen ? 'navbar__links--open' : ''}`}>
          {links.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              className={`navbar__link ${pathname === to ? 'navbar__link--active' : ''}`}
              onClick={() => setMenuOpen(false)}
            >
              {label}
            </Link>
          ))}
        </div>

        <div className="navbar__actions">
          <button className="navbar__theme-btn" onClick={toggle} aria-label="Перемкнути тему">
            {theme === 'light' ? '🌙' : '☀️'}
          </button>
          <Link to="/login" className="btn btn--outline navbar__btn-sm">Увійти</Link>
          <Link to="/register" className="btn btn--primary navbar__btn-sm">Реєстрація</Link>
        </div>

        <button
          className="navbar__burger"
          onClick={() => setMenuOpen(o => !o)}
          aria-label="Меню"
        >
          <span /><span /><span />
        </button>
      </div>
    </nav>
  );
}
