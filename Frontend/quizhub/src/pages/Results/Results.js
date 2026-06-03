import { useState, useEffect } from 'react';
import { Link, useParams, useLocation, useNavigate } from 'react-router-dom';
import { getApiJson } from '../../api';
import './Results.scss';

function ScoreRing({ percent }) {
  const r = 54;
  const circ = 2 * Math.PI * r;
  const dash = (percent / 100) * circ;
  return (
    <svg className="results__ring" viewBox="0 0 130 130" width="130" height="130">
      <circle cx="65" cy="65" r={r} fill="none" strokeWidth="10" className="results__ring-bg" />
      <circle
        cx="65" cy="65" r={r} fill="none" strokeWidth="10"
        strokeDasharray={`${dash} ${circ}`}
        strokeLinecap="round"
        className="results__ring-fill"
        transform="rotate(-90 65 65)"
      />
      <text x="65" y="60" textAnchor="middle" className="results__ring-num">{percent}%</text>
      <text x="65" y="76" textAnchor="middle" className="results__ring-lbl">результат</text>
    </svg>
  );
}

export default function Results() {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const { accauntId, sessionId } = location.state || {};

  useEffect(() => {
    if (!accauntId || !sessionId) { navigate(`/quizzes/${id}/take`); return; }
    getApiJson(`/api/get_test_result/${accauntId}/${sessionId}`)
      .then(setData)
      .catch(err => {
        console.error(err);
        if (err?.message?.includes('HTTP 401')) {
          navigate('/login');
        }
      })
      .finally(() => setLoading(false));
  }, [id, accauntId, sessionId, navigate]);

  if (loading) return <div className="container">Завантаження...</div>;
  if (!data) return (
    <div className="container" style={{ padding: '2rem' }}>
      <p>Немає даних. <Link to={`/quizzes/${id}/take`}>Пройти тест</Link></p>
    </div>
  );

  const questions = data.questions || [];
  const total = questions.length;
  const correct = questions.filter(q => q.userAnswered === q.correctAnswer).length;
  const percent = total > 0 ? Math.round((correct / total) * 100) : 0;
  const passed = percent >= 60;

  return (
    <div className="results">
      <div className="container">
        <div className="results__hero">
          <ScoreRing percent={percent} />
          <div className="results__summary">
            <div className={`results__badge ${passed ? 'results__badge--pass' : 'results__badge--fail'}`}>
              {passed ? '🎉 Пройдено!' : '😞 Не пройдено'}
            </div>
            <h1>Результати тесту</h1>
            <div className="results__stats">
              <div className="results__stat">
                <span className="results__stat-val">{correct}/{total}</span>
                <span className="results__stat-lbl">правильних</span>
              </div>
              <div className="results__stat">
                <span className="results__stat-val">{total - correct}</span>
                <span className="results__stat-lbl">помилок</span>
              </div>
              <div className="results__stat">
                <span className="results__stat-val">{data.score}</span>
                <span className="results__stat-lbl">балів</span>
              </div>
            </div>
            <div className="results__actions">
              <Link to={`/quizzes/${id}/take`} className="btn btn--outline">Пройти знову</Link>
              <Link to="/quizzes" className="btn btn--primary">Інші тести</Link>
            </div>
          </div>
        </div>
        <div className="results__breakdown">
          <h2>Розбір відповідей</h2>
          {questions.map((q, i) => {
            const ok = q.userAnswered === q.correctAnswer;
            return (
              <div key={i} className={`results__answer ${ok ? 'results__answer--ok' : 'results__answer--wrong'}`}>
                <div className="results__answer-head">
                  <span className="results__answer-icon">{ok ? '✓' : '✗'}</span>
                  <span className="results__answer-q">{q.question}</span>
                </div>
                {!ok && (
                  <div className="results__answer-detail">
                    <span className="results__answer-wrong-lbl">Ваша відповідь: <b>{q.userAnswered || '—'}</b></span>
                    <span className="results__answer-correct-lbl">Правильно: <b>{q.correctAnswer}</b></span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}