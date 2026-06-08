import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { postApiJson, getApiJson, getStoredAccaunt, API_BASE } from '../../api';
import './CreateQuiz.scss';

const EMPTY_Q = () => ({ id: Date.now(), text: '', options: ['', '', '', ''], correct: 0 });

export default function CreateQuiz() {
  const navigate = useNavigate();
  const { id } = useParams();
  const isEditMode = Boolean(id);
  const [meta, setMeta] = useState({ title: '', category: 'Програмування' });
  const [questions, setQuestions] = useState([EMPTY_Q()]);
  const [publishing, setPublishing] = useState(false);
  const [loading, setLoading] = useState(isEditMode);
  const [error, setError] = useState('');
  const [loadError, setLoadError] = useState('');

  const setMF = k => e => setMeta(p => ({ ...p, [k]: e.target.value }));

  const addQ = () => setQuestions(p => [...p, EMPTY_Q()]);
  const removeQ = i => setQuestions(p => p.filter((_, idx) => idx !== i));
  const setQText = (i, v) => setQuestions(p => p.map((q, idx) => idx === i ? { ...q, text: v } : q));
  const setOpt = (qi, oi, v) => setQuestions(p => p.map((q, idx) => idx === qi ? { ...q, options: q.options.map((o, j) => j === oi ? v : o) } : q));
  const setCorrect = (qi, oi) => setQuestions(p => p.map((q, idx) => idx === qi ? { ...q, correct: oi } : q));

  const normalizeAnswers = answers => {
    if (Array.isArray(answers)) return answers;
    if (typeof answers === 'string') {
      try { return JSON.parse(answers); } catch (e) { return []; }
    }
    return [];
  };

  useEffect(() => {
    if (!isEditMode) return;

    const stored = getStoredAccaunt();
    if (!stored?.access) {
      navigate('/login');
      return;
    }

    setLoading(true);
    setLoadError('');

    getApiJson(`/api/tests/${id}`, { auth: true })
      .then(test => {
        setMeta({ title: test.name || '', category: test.category || 'Програмування' });
        const questionItems = test.questions || [];
        setQuestions(questionItems.length ? questionItems.map(q => {
          const answers = normalizeAnswers(q.answers).concat(['', '', '', '']).slice(0, 4);
          const correctIdx = answers.findIndex(a => a === q.correctAnswer);
          return {
            id: q.id || Date.now(),
            questionId: q.questionId || null,
            text: q.question || '',
            options: answers,
            correct: correctIdx >= 0 ? correctIdx : 0,
          };
        }) : [EMPTY_Q()]);
      })
      .catch(() => {
        setLoadError('Не вдалося завантажити тест для редагування');
      })
      .finally(() => {
        setLoading(false);
      });
  }, [id, isEditMode, navigate]);

  const publish = async () => {
    setError('');

    if (!meta.title.trim()) { setError('Введіть назву тесту'); return; }

    const invalid = questions.find(q => !q.text.trim() || q.options.some(o => !o.trim()));
    if (invalid) { setError('Заповніть усі питання та варіанти відповідей'); return; }

    setPublishing(true);
    try {
      if (isEditMode) {
        const stored = getStoredAccaunt();
        if (!stored?.access) {
          navigate('/login');
          return;
        }

        await fetch(`${API_BASE}/api/tests/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            Accept: 'application/json',
            Authorization: `Bearer ${stored.access}`,
          },
          body: JSON.stringify({
            name: meta.title.trim(),
            category: String(meta.category || 'Програмування'),
            questions: questions.map(q => ({
              questionId: q.questionId,
              id: q.id,
              question: q.text.trim(),
              answers: q.options.map(opt => String(opt || '')),
              correctAnswer: String(q.options[q.correct] || ''),
              score: 10,
            })),
          }),
        });

        navigate(`/quizzes/${id}`);
        return;
      }

      const testRes = await postApiJson('/api/create_test', {
        name: meta.title.trim(),
        category: String(meta.category || 'Програмування'),
      }, { auth: true });

      const testId = testRes.test?.id || testRes.id;

      const questionIds = [];
      for (const q of questions) {
        const qRes = await postApiJson('/api/create_question', {
          question: q.text.trim(),
          answers: q.options,
          correctAnswer: q.options[q.correct],
          score: 10,
        }, { auth: true });
        questionIds.push(qRes.question?.id || qRes.id);
      }

      await postApiJson('/api/add_questions_to_test', {
        testId,
        questionsIds: questionIds,
      }, { auth: true });

      navigate(`/quizzes/${testId}`);
    } catch (err) {
      setError(err.message || 'Помилка публікації');
    } finally {
      setPublishing(false);
    }
  };

  if (loading) {
    return (
      <div className="create-quiz">
        <div className="container">
          <div className="page-header">
            <h1>{isEditMode ? 'Редагувати тест' : 'Створити тест'}</h1>
            <p>Завантаження даних тесту...</p>
          </div>
          {loadError ? <p className="create-quiz__error">{loadError}</p> : <p>Зачекайте, будь ласка...</p>}
        </div>
      </div>
    );
  }

  return (
    <div className="create-quiz">
      <div className="container">
        <div className="page-header">
          <h1>{isEditMode ? 'Редагувати тест' : 'Створити тест'}</h1>
          <p>Заповни основну інформацію та додай питання</p>
        </div>

        <div className="create-quiz__layout">
          <div className="create-quiz__main">

            <section className="create-quiz__block">
              <h2>Основна інформація</h2>
              <div className="create-quiz__field">
                <label>Назва тесту</label>
                <input type="text" placeholder="Наприклад: Основи Python" value={meta.title} onChange={setMF('title')} />
              </div>
              <div className="create-quiz__field">
                <label>Категорія</label>
                <select value={meta.category} onChange={setMF('category')}>
                  {['Програмування', 'Математика', 'Мови', 'Наука', 'Історія'].map(c => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>
            </section>

            <section className="create-quiz__block">
              <div className="create-quiz__q-head">
                <h2>Питання ({questions.length})</h2>
                <button className="btn btn--outline create-quiz__add-btn" onClick={addQ}>+ Додати</button>
              </div>

              {questions.map((q, qi) => (
                <div key={q.id} className="create-quiz__question">
                  <div className="create-quiz__q-topbar">
                    <span className="create-quiz__q-num">Питання {qi + 1}</span>
                    {questions.length > 1 && (
                      <button className="create-quiz__q-remove" onClick={() => removeQ(qi)}>✕</button>
                    )}
                  </div>
                  <div className="create-quiz__field">
                    <label>Текст питання</label>
                    <input type="text" placeholder="Введіть питання..." value={q.text} onChange={e => setQText(qi, e.target.value)} />
                  </div>
                  <div className="create-quiz__options-grid">
                    {q.options.map((opt, oi) => (
                      <div key={oi} className={`create-quiz__option-row ${q.correct === oi ? 'create-quiz__option-row--correct' : ''}`}>
                        <button
                          className="create-quiz__correct-btn"
                          onClick={() => setCorrect(qi, oi)}
                          title="Позначити як правильну"
                        >
                          {q.correct === oi ? '✓' : String.fromCharCode(65 + oi)}
                        </button>
                        <input
                          type="text"
                          placeholder={`Варіант ${String.fromCharCode(65 + oi)}`}
                          value={opt}
                          onChange={e => setOpt(qi, oi, e.target.value)}
                        />
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </section>
          </div>

          <aside className="create-quiz__sidebar">
            <div className="create-quiz__publish-card">
              <h3>Публікація</h3>
              {error && <p className="create-quiz__error">{error}</p>}
              <button
                className="btn btn--primary create-quiz__publish-btn"
                onClick={publish}
                disabled={publishing}
              >
                {publishing ? (isEditMode ? 'Зберігаю...' : 'Публікую...') : (isEditMode ? 'Зберегти зміни' : 'Опублікувати тест')}
              </button>
              <div className="create-quiz__publish-info">
                <span>{questions.length} питань</span>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  );
}