import { Link, useParams } from 'react-router-dom';
import './Results.scss';

const RESULT = {
  score: 17,
  total: 20,
  percent: 85,
  time: '12 хв 34 сек',
  quizTitle: 'Основи Python',
  answers: [
    { q: 'Який оператор використовується для порівняння?', correct: '==', chosen: '==', ok: true },
    { q: 'Яка функція виводить текст у консоль?', correct: 'print()', chosen: 'print()', ok: true },
    { q: 'Як оголосити список у Python?', correct: 'list = []', chosen: 'list = ()', ok: false },
  ],
};

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
  const passed = RESULT.percent >= 60;

  return (
    <div className="results">
      <div className="container">
        <div className="results__hero">
          <ScoreRing percent={RESULT.percent} />
          <div className="results__summary">
            <div className={`results__badge ${passed ? 'results__badge--pass' : 'results__badge--fail'}`}>
              {passed ? '🎉 Пройдено!' : '😞 Не пройдено'}
            </div>
            <h1>{RESULT.quizTitle}</h1>
            <div className="results__stats">
              <div className="results__stat">
                <span className="results__stat-val">{RESULT.score}/{RESULT.total}</span>
                <span className="results__stat-lbl">правильних</span>
              </div>
              <div className="results__stat">
                <span className="results__stat-val">{RESULT.total - RESULT.score}</span>
                <span className="results__stat-lbl">помилок</span>
              </div>
              <div className="results__stat">
                <span className="results__stat-val">{RESULT.time}</span>
                <span className="results__stat-lbl">витрачено</span>
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
          {RESULT.answers.map((a, i) => (
            <div key={i} className={`results__answer ${a.ok ? 'results__answer--ok' : 'results__answer--wrong'}`}>
              <div className="results__answer-head">
                <span className="results__answer-icon">{a.ok ? '✓' : '✗'}</span>
                <span className="results__answer-q">{a.q}</span>
              </div>
              {!a.ok && (
                <div className="results__answer-detail">
                  <span className="results__answer-wrong-lbl">Ваша відповідь: <b>{a.chosen}</b></span>
                  <span className="results__answer-correct-lbl">Правильно: <b>{a.correct}</b></span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
