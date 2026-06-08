import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getApiJson, getStoredAccaunt, API_BASE } from '../../api';
import './TeacherDashboard.scss';

export default function TeacherDashboard() {
  const navigate = useNavigate();
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [accaunt, setAccaunt] = useState(null);

  useEffect(() => {
    const stored = getStoredAccaunt();
    if (!stored?.accaunt) { navigate('/login'); return; }
    setAccaunt(stored.accaunt);

    getApiJson('/api/tests')
      .then(data => {
        const mine = (data || []).filter(t => t.author?.id === stored.accaunt.id);
        setQuizzes(mine);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [navigate]);

  const deleteQuiz = async (quizId) => {
    if (!window.confirm('Видалити тест? Ця дія незворотна.')) {
      return;
    }

    const stored = getStoredAccaunt();
    if (!stored?.access) {
      navigate('/login');
      return;
    }

    try {
      const response = await fetch(`${API_BASE}/api/tests/${quizId}`, {
        method: 'DELETE',
        headers: {
          Accept: 'application/json',
          Authorization: `Bearer ${stored.access}`,
        },
      });

      if (!response.ok) {
        const body = await response.text();
        throw new Error(body || 'Не вдалося видалити тест');
      }

      setQuizzes(prev => prev.filter(q => q.id !== quizId));
    } catch (err) {
      console.error('delete test', err);
      alert('Не вдалося видалити тест. Спробуйте ще раз.');
    }
  };

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
            { icon: '📝', val: loading ? '...' : quizzes.length, lbl: 'Тестів' },
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
          {loading ? (
            <p style={{ opacity: 0.5 }}>Завантаження...</p>
          ) : quizzes.length === 0 ? (
            <p style={{ opacity: 0.5 }}>Ви ще не створили жодного тесту. <Link to="/teacher/create">Створити перший →</Link></p>
          ) : (
            <div className="teacher__table">
              <div className="teacher__table-head">
                <span>Назва</span>
                <span>Категорія</span>
                <span>Питань</span>
                <span>Дії</span>
              </div>
              {quizzes.map(q => (
                <div key={q.id} className="teacher__table-row">
                  <span className="teacher__quiz-title">{q.name}</span>
                  <span>{q.category}</span>
                  <span>{q.questions?.length || 0}</span>
                  <div className="teacher__row-actions">
                    <Link to={`/teacher/edit/${q.id}`} className="teacher__action-btn">✎</Link>
                    <button
                      type="button"
                      className="teacher__action-btn teacher__action-btn--del"
                      onClick={() => deleteQuiz(q.id)}
                    >
                      🗑
                    </button>
                    <Link to={`/quizzes/${q.id}`} className="teacher__action-btn">📊</Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}