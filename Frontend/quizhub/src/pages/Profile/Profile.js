import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Profile.scss';

export default function Profile() {
  const navigate = useNavigate();
  const [accaunt, setAccaunt] = useState(null);

  useEffect(() => {
    const stored = localStorage.getItem('accaunt');
    if (!stored) { navigate('/login'); return; }
    const parsed = JSON.parse(stored);
    setAccaunt(parsed.accaunt || parsed);
  }, [navigate]);

  if (!accaunt) return null;

  const initials = accaunt.name
    ?.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2) || '??';

  return (
    <div className="profile">
      <div className="container">
        <div className="profile__hero">
          <div className="profile__avatar">{initials}</div>
          <div className="profile__info">
            <h1>{accaunt.name}</h1>
            <p>{accaunt.login}</p>
            <span className="profile__role">{accaunt.isTeacher ? 'Вчитель' : 'Студент'}</span>
          </div>
          <button className="btn btn--outline profile__edit-btn">Редагувати профіль</button>
        </div>
        <div className="profile__stats">
          {[
            { icon: '✅', val: '—', lbl: 'Тестів пройдено' },
            { icon: '📊', val: '—', lbl: 'Середній бал' },
            { icon: '🏆', val: '—', lbl: 'Топ результатів' },
            { icon: '🔥', val: '—', lbl: 'Днів поспіль' },
          ].map(s => (
            <div key={s.lbl} className="profile__stat">
              <span className="profile__stat-icon">{s.icon}</span>
              <span className="profile__stat-val">{s.val}</span>
              <span className="profile__stat-lbl">{s.lbl}</span>
            </div>
          ))}
        </div>
        <div className="profile__section">
          <h2>Історія проходжень</h2>
          <p style={{ opacity: 0.5 }}>Буде доступно після додавання відповідного API</p>
        </div>
      </div>
    </div>
  );
}