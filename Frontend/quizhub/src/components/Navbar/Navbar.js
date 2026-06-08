import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useTheme } from '../../context/ThemeContext';
import { getStoredAccaunt, clearSession } from '../../api';
import './Navbar.scss';

export default function Navbar() {
  const { theme, toggle } = useTheme();
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const [menuOpen, setMenuOpen] = useState(false);
  const [accaunt, setAccaunt] = useState(null);

  useEffect(() => {
    const stored = getStoredAccaunt();
    setAccaunt(stored?.accaunt || null);
  }, [pathname]); // перечитываем при каждом переходе

  const logout = () => {
    clearSession();
    setAccaunt(null);
    navigate('/');
  };

  const links = [
    { to: '/', label: 'Головна' },
    { to: '/quizzes', label: 'Тести' },
  ];

  const initials = accaunt?.name
    ?.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2) || '?';

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

          {accaunt ? (
            <>
              <div className="navbar__user">
                <Link to="/profile" className="navbar__avatar" title={accaunt.name}>
                  {initials}
                </Link>
                <div className="navbar__user-info">
                  <span className="navbar__user-name">{accaunt.name}</span>
                  <span className="navbar__user-role">{accaunt.isTeacher ? 'Учитель' : 'Учасник'}</span>
                </div>
              </div>
              {accaunt.isTeacher && (
                <Link to="/teacher" className="btn btn--outline navbar__btn-sm">Кабінет</Link>
              )}
              <button className="btn btn--outline navbar__btn-sm" onClick={logout}>Вийти</button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn--outline navbar__btn-sm">Увійти</Link>
              <Link to="/register" className="btn btn--primary navbar__btn-sm">Реєстрація</Link>
            </>
          )}
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