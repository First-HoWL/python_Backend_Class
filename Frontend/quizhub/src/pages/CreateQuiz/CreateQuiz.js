import { useState } from 'react';
import { useParams } from 'react-router-dom';
import './CreateQuiz.scss';

const EMPTY_Q = () => ({ id: Date.now(), text: '', options: ['', '', '', ''], correct: 0 });

export default function CreateQuiz() {
  const { id } = useParams();
  const isEdit = Boolean(id);

  const [meta, setMeta] = useState({ title: '', description: '', category: 'Програмування', difficulty: 'Середнє' });
  const [questions, setQuestions] = useState([EMPTY_Q()]);
  const [aiTopic, setAiTopic] = useState('');
  const [aiCount, setAiCount] = useState(5);
  const [aiLoading, setAiLoading] = useState(false);

  const setMF = k => e => setMeta(p => ({ ...p, [k]: e.target.value }));

  const addQ = () => setQuestions(p => [...p, EMPTY_Q()]);
  const removeQ = i => setQuestions(p => p.filter((_, idx) => idx !== i));
  const setQText = (i, v) => setQuestions(p => p.map((q, idx) => idx === i ? { ...q, text: v } : q));
  const setOpt = (qi, oi, v) => setQuestions(p => p.map((q, idx) => idx === qi ? { ...q, options: q.options.map((o, j) => j === oi ? v : o) } : q));
  const setCorrect = (qi, oi) => setQuestions(p => p.map((q, idx) => idx === qi ? { ...q, correct: oi } : q));

  const simulateAI = () => {
    setAiLoading(true);
    setTimeout(() => {
      const generated = Array.from({ length: aiCount }, (_, i) => ({
        ...EMPTY_Q(),
        text: `AI-питання ${i + 1} по темі "${aiTopic}"`,
        options: ['Варіант A', 'Варіант B', 'Варіант C', 'Варіант D'],
        correct: 0,
      }));
      setQuestions(p => [...p.filter(q => q.text), ...generated]);
      setAiLoading(false);
    }, 1400);
  };

  return (
    <div className="create-quiz">
      <div className="container">
        <div className="page-header">
          <h1>{isEdit ? 'Редагувати тест' : 'Створити тест'}</h1>
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
                <label>Опис</label>
                <textarea rows={3} placeholder="Короткий опис тесту..." value={meta.description} onChange={setMF('description')} />
              </div>
              <div className="create-quiz__row">
                <div className="create-quiz__field">
                  <label>Категорія</label>
                  <select value={meta.category} onChange={setMF('category')}>
                    {['Програмування', 'Математика', 'Мови', 'Наука', 'Історія'].map(c => (
                      <option key={c}>{c}</option>
                    ))}
                  </select>
                </div>
                <div className="create-quiz__field">
                  <label>Складність</label>
                  <select value={meta.difficulty} onChange={setMF('difficulty')}>
                    {['Легко', 'Середнє', 'Важко'].map(d => <option key={d}>{d}</option>)}
                  </select>
                </div>
              </div>
            </section>

            <section className="create-quiz__block create-quiz__ai-block">
              <div className="create-quiz__ai-head">
                <div>
                  <h2>AI-генерація питань</h2>
                  <p>Gemini 2.0 Flash згенерує питання за темою</p>
                </div>
              </div>
              <div className="create-quiz__row">
                <div className="create-quiz__field" style={{ flex: 2 }}>
                  <label>Тема для генерації</label>
                  <input type="text" placeholder="Наприклад: списки та словники в Python" value={aiTopic} onChange={e => setAiTopic(e.target.value)} />
                </div>
                <div className="create-quiz__field">
                  <label>Кількість питань</label>
                  <select value={aiCount} onChange={e => setAiCount(Number(e.target.value))}>
                    {[3, 5, 10, 15, 20].map(n => <option key={n}>{n}</option>)}
                  </select>
                </div>
              </div>
              <button
                className="btn btn--ghost create-quiz__ai-btn"
                onClick={simulateAI}
                disabled={!aiTopic || aiLoading}
              >
                {aiLoading ? 'Генерую...' : 'Згенерувати питання'}
              </button>
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
              <button className="btn btn--primary create-quiz__publish-btn">
                {isEdit ? 'Зберегти зміни' : 'Опублікувати тест'}
              </button>
              <button className="btn btn--outline create-quiz__publish-btn">
                Зберегти як чернетку
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
