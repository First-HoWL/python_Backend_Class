import { Link } from 'react-router-dom';
import './TeacherDashboard.scss';

const MY_QUIZZES = [
  { id: 1, title: 'Основи Python', questions: 20, attempts: 342, avg: 78, status: 'active' },
  { id: 2, title: 'JavaScript основи', questions: 25, attempts: 211, avg: 72, status: 'active' },
  { id: 3, title: 'ООП концепції', questions: 15, attempts: 89, avg: 65, status: 'draft' },
];

export default function TeacherDashboard() {
  return (
    <div className="teacher">
      <div className="container">
        <div className="teacher__topbar">
          <div>
            <h1>Кабінет вчителя</h1>
            <p>Керуй своїми тестами та переглядай статистику</p>
          </div>
          <Link to="/teacher/create" className="btn btn--primary">
            + Створити тест
          </Link>
        </div>

        <div className="teacher__stats">
          {[
            { icon: '📝', val: 3, lbl: 'Тестів' },
            { icon: '👥', val: 642, lbl: 'Проходжень' },
            { icon: '📊', val: '72%', lbl: 'Середній бал' },
            { icon: '⭐', val: 4.7, lbl: 'Рейтинг' },
          ].map(s => (
            <div key={s.lbl} className="teacher__stat-card">
              <span className="teacher__stat-icon">{s.icon}</span>
              <span className="teacher__stat-val">{s.val}</span>
              <span className="teacher__stat-lbl">{s.lbl}</span>
            </div>
          ))}
        </div>

        <div className="teacher__section">
          <h2>Мої тести</h2>
          <div className="teacher__table">
            <div className="teacher__table-head">
              <span>Назва</span>
              <span>Питань</span>
              <span>Проходжень</span>
              <span>Середній бал</span>
              <span>Статус</span>
              <span>Дії</span>
            </div>
            {MY_QUIZZES.map(q => (
              <div key={q.id} className="teacher__table-row">
                <span className="teacher__quiz-title">{q.title}</span>
                <span>{q.questions}</span>
                <span>{q.attempts}</span>
                <span>
                  <span className="teacher__avg">{q.avg}%</span>
                </span>
                <span>
                  <span className={`teacher__status teacher__status--${q.status}`}>
                    {q.status === 'active' ? 'Активний' : 'Чернетка'}
                  </span>
                </span>
                <div className="teacher__row-actions">
                  <Link to={`/teacher/edit/${q.id}`} className="teacher__action-btn">✏️</Link>
                  <Link to={`/quizzes/${q.id}`} className="teacher__action-btn">📊</Link>
                  <button className="teacher__action-btn teacher__action-btn--del">🗑</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
