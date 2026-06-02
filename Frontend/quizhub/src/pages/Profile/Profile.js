import './Profile.scss';

const HISTORY = [
  { id: 1, title: 'Основи Python', score: 17, total: 20, percent: 85, date: '28 трав 2025' },
  { id: 2, title: 'Алгебра 9 клас', score: 12, total: 15, percent: 80, date: '25 трав 2025' },
  { id: 3, title: 'Англійська B1', score: 22, total: 30, percent: 73, date: '20 трав 2025' },
];

export default function Profile() {
  return (
    <div className="profile">
      <div className="container">
        <div className="profile__hero">
          <div className="profile__avatar">КМ</div>
          <div className="profile__info">
            <h1>Катерина Мельник</h1>
            <p>katya@example.com</p>
            <span className="profile__role">Студент</span>
          </div>
          <button className="btn btn--outline profile__edit-btn">Редагувати профіль</button>
        </div>

        <div className="profile__stats">
          {[
            { icon: '✅', val: 12, lbl: 'Тестів пройдено' },
            { icon: '📊', val: '78%', lbl: 'Середній бал' },
            { icon: '🏆', val: 3, lbl: 'Топ результатів' },
            { icon: '🔥', val: 7, lbl: 'Днів поспіль' },
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
          <div className="profile__history">
            {HISTORY.map(h => (
              <div key={h.id} className="profile__history-row">
                <div className="profile__history-info">
                  <span className="profile__history-title">{h.title}</span>
                  <span className="profile__history-date">{h.date}</span>
                </div>
                <div className="profile__history-result">
                  <span className="profile__history-score">{h.score}/{h.total}</span>
                  <span className={`profile__history-pct ${h.percent >= 80 ? 'profile__history-pct--good' : h.percent >= 60 ? 'profile__history-pct--mid' : 'profile__history-pct--low'}`}>
                    {h.percent}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}