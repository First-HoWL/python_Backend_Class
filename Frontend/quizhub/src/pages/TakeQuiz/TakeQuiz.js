import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getApiJson } from '../../api';
import './TakeQuiz.scss';

export default function TakeQuiz() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    getApiJson('/api/tests')
      .then(data => {
        const t = data.find(x => String(x.id) === String(id));
        if (t && t.questions) {
          const mapped = t.questions.map(q => ({ id: q.questionId || q.id, text: q.question || q.text, options: q.answers || q.options || [] }));
          setQuestions(mapped);
        } else {
          setQuestions([]);
        }
      })
      .catch((err) => { console.error('Failed to load test questions', err); setQuestions([]); });
  }, [id]);

  if (questions.length === 0) return <div className="container">Питання завантажуються або не знайдені...</div>;

  const q = questions[current];
  const progress = ((current + 1) / questions.length) * 100;
  const isLast = current === questions.length - 1;

  const select = (opt) => setAnswers(prev => ({ ...prev, [q.id]: opt }));

  const next = () => {
    if (isLast) {
      navigate(`/quizzes/${id}/results/1`);
    } else {
      setCurrent(c => c + 1);
    }
  };

  return (
    <div className="take-quiz">
      <div className="container">
        <div className="take-quiz__header">
          <span className="take-quiz__title">Тест #{id}</span>
          <span className="take-quiz__counter">{current + 1} / {questions.length}</span>
        </div>

        <div className="take-quiz__progress">
          <div className="take-quiz__progress-bar" style={{ width: `${progress}%` }} />
        </div>

        <div className="take-quiz__card">
          <p className="take-quiz__num">Питання {current + 1}</p>
          <h2 className="take-quiz__question">{q.text}</h2>

          <div className="take-quiz__options">
            {q.options.map((opt, i) => (
              <button
                key={i}
                className={`take-quiz__option ${answers[q.id] === opt ? 'take-quiz__option--selected' : ''}`}
                onClick={() => select(opt)}
              >
                <span className="take-quiz__option-letter">{String.fromCharCode(65 + i)}</span>
                {opt}
              </button>
            ))}
          </div>

          <div className="take-quiz__actions">
            {current > 0 && (
              <button className="btn btn--outline" onClick={() => setCurrent(c => c - 1)}>
                ← Назад
              </button>
            )}
            <button
              className="btn btn--primary"
              onClick={next}
              disabled={!answers[q.id]}
            >
              {isLast ? 'Завершити тест' : 'Далі →'}
            </button>
          </div>
        </div>

        <div className="take-quiz__dots">
          {questions.map((_, i) => (
            <div
              key={i}
              className={`take-quiz__dot ${i === current ? 'take-quiz__dot--active' : ''} ${answers[questions[i].id] ? 'take-quiz__dot--answered' : ''}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
