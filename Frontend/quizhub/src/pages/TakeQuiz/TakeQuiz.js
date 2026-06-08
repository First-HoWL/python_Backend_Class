import { useState, useEffect, useRef } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getApiJson, postApiJson, getStoredAccaunt } from '../../api';
import './TakeQuiz.scss';

export default function TakeQuiz() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState({});
  const [questions, setQuestions] = useState([]);
  const [quizTitle, setQuizTitle] = useState('Тест');
  const [sessionId, setSessionId] = useState(null);
  const [loadError, setLoadError] = useState('');
  const [submitError, setSubmitError] = useState('');
  const [loading, setLoading] = useState(true);
  const [dotsExpanded, setDotsExpanded] = useState(false);
  const sessionCreated = useRef(false);

  useEffect(() => {
    // Читаем сохранённый объект. После логина бэкенд возвращает:
    // { access, refresh, accaunt: { id, login, name, isTeacher } }
    const stored = getStoredAccaunt();

    if (!stored) {
      navigate('/login');
      return;
    }

    // Токен лежит в корне объекта: stored.access
    const authToken = stored.access;
    if (!authToken) {
      // Нет токена — сессия невалидна, отправляем на логин
      // clear in-memory session
      import('../../api').then(mod => mod.clearSession()).catch(()=>{});
      navigate('/login');
      return;
    }

    // Данные пользователя вложены в stored.accaunt
    const accauntData = stored.accaunt;
    if (!accauntData?.id) {
      import('../../api').then(mod => mod.clearSession()).catch(()=>{});
      navigate('/login');
      return;
    }

    const loadQuiz = async () => {
      try {
        const data = await getApiJson('/api/tests');
        const t = data.find(x => String(x.id) === String(id));
        if (!t) {
          throw new Error('Тест не знайдено');
        }

        setQuizTitle(t.name || t.title || `Тест #${id}`);
        setQuestions((t.questions || []).map(q => {
          let options = q.answers || [];
          if (typeof options === 'string') {
            try { options = JSON.parse(options.replace(/'/g, '"')); } catch { options = []; }
          }
          if (!Array.isArray(options)) {
            options = [];
          }
          return {
            id: q.id,
            questionId: q.questionId ?? q.id,
            text: q.question || q.text || 'Без тексту питання',
            options,
            score: q.score || 0,
          };
        }));

        if (!sessionCreated.current) {
          sessionCreated.current = true;
            try {
            const session = await postApiJson(
              '/api/create_session',
              { testId: Number(id) },
              { auth: true }
            );
            setSessionId(session.sessionId);
            } catch (err) {
            const message = err?.message || '';
            if (message.includes('HTTP 401')) {
              sessionCreated.current = false; // сбрасываем флаг чтобы можно было повторити
              import('../../api').then(mod => mod.clearSession()).catch(()=>{});
              navigate('/login');
              return;
            }
            throw err;
          }
        }
      } catch (err) {
        const message = err?.message || 'Не вдалося завантажити тест';
        if (message.includes('HTTP 401')) {
          import('../../api').then(mod => mod.clearSession()).catch(()=>{});
          navigate('/login');
          return;
        }
        setLoadError(message);
      } finally {
        setLoading(false);
      }
    };

    loadQuiz();
  }, [id, navigate]);

  if (loadError) return (
    <div className="container" style={{ padding: '2rem', color: 'red' }}>
      {loadError}
    </div>
  );

  if (loading) return <div className="container">Завантаження...</div>;

  // Тест загружен, но сессия ещё не создана — показываем загрузку
  if (!sessionId) return <div className="container">Створення сесії...</div>;

  if (questions.length === 0) return <div className="container">Питань не знайдено.</div>;

  const q = questions[current];
  const answeredCount = Object.keys(answers).length;
  const progress = ((current + 1) / questions.length) * 100;
  const isLast = current === questions.length - 1;

  const select = opt => {
    setSubmitError('');
    setAnswers(prev => ({ ...prev, [q.id]: opt }));
  };

  const next = async () => {
    if (!answers[q.id]) {
      setSubmitError('Оберіть відповідь перед переходом далі.');
      return;
    }

    // Берём accauntData из localStorage заново на случай обновления
    const stored = getStoredAccaunt();
    if (!stored?.accaunt?.id) {
      navigate('/login');
      return;
    }

    const questionId = q.questionId ?? q.id;

    try {
      await postApiJson(
        '/api/answer_question',
        {
          sessionId,
          questionId,
          answer: answers[q.id],
        },
        { auth: true }
      );
      } catch (err) {
      console.error('answer_question:', err);
      const message = err?.message || '';
      if (message.includes('HTTP 401')) {
        import('../../api').then(mod => mod.clearSession()).catch(()=>{});
        navigate('/login');
        return;
      }
      setSubmitError('Не вдалося надіслати відповідь. Спробуйте ще раз.');
      return;
    }

    if (isLast) {
      navigate(`/quizzes/${id}/results`, {
        state: {
          accauntId: stored.accaunt.id,
          sessionId,
        },
      });
    } else {
      setCurrent(c => c + 1);
    }
  };

  return (
    <div className="take-quiz">
      <div className="container">
        <div className="take-quiz__header">
          <div>
            <span className="take-quiz__title">{quizTitle}</span>
            <div className="take-quiz__subtitle">Питання {current + 1} з {questions.length}</div>
          </div>
          <span className="take-quiz__counter">{current + 1} / {questions.length}</span>
        </div>
        <div className="take-quiz__progress">
          <div className="take-quiz__progress-bar" style={{ width: `${progress}%` }} />
        </div>
        <div className="take-quiz__card">
          <p className="take-quiz__num">Питання {current + 1}</p>
          <h2 className="take-quiz__question">{q.text}</h2>
          <div className="take-quiz__options">
            {(Array.isArray(q.options) ? q.options : []).map((opt, i) => (
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
          {submitError && <div className="take-quiz__error">{submitError}</div>}
          <div className="take-quiz__actions">
            {current > 0 && (
              <button className="btn btn--outline" onClick={() => setCurrent(c => c - 1)}>← Назад</button>
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
        <div className="take-quiz__dots-panel">
          <div className="take-quiz__dots-info">
            <div className="take-quiz__dots-summary">
              Відповіли: <strong>{answeredCount}</strong> з {questions.length}
            </div>
            <button
              type="button"
              className={`btn btn--outline btn--sm take-quiz__dots-toggle ${dotsExpanded ? 'take-quiz__dots-toggle--open' : ''}`}
              onClick={() => setDotsExpanded(open => !open)}
            >
              {dotsExpanded ? 'Приховати всі' : 'Показати всі питання'}
            </button>
          </div>
        </div>
        <div className={`take-quiz__dots ${dotsExpanded ? 'take-quiz__dots--expanded' : ''}`}>
          {questions.map((question, i) => {
            const answered = Boolean(answers[question.id]);
            return (
              <button
                key={i}
                type="button"
                className={`take-quiz__dot
                  ${i === current ? 'take-quiz__dot--active' : ''}
                  ${answered ? 'take-quiz__dot--answered' : ''}
                `}
                onClick={() => setCurrent(i)}
                aria-label={`Перейти до питання ${i + 1}${answered ? ', відповіли' : ''}`}
              >
                {dotsExpanded ? i + 1 : null}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}