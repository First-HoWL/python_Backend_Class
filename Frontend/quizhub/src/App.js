import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import { getStoredAccaunt } from './api';

import Home from './pages/Home/Home';
import AllQuizzes from './pages/AllQuizzes/AllQuizzes';
import QuizDetail from './pages/QuizDetail/QuizDetail';
import TakeQuiz from './pages/TakeQuiz/TakeQuiz';
import Results from './pages/Results/Results';
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import TeacherDashboard from './pages/TeacherDashboard/TeacherDashboard';
import CreateQuiz from './pages/CreateQuiz/CreateQuiz';
import Profile from './pages/Profile/Profile';
import NotFound from './pages/NotFound/NotFound';

import './styles/global.scss';

// Защищённый роут — если нет токена, редиректит на /login
function PrivateRoute({ children }) {
  const session = getStoredAccaunt();
  if (!session?.access) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

function TeacherRoute({ children }) {
  const session = getStoredAccaunt();
  if (!session?.access) {
    return <Navigate to="/login" replace />;
  }
  if (!session?.accaunt?.isTeacher) {
    return <Navigate to="/" replace />;
  }
  return children;
}

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Navbar />
          <main style={{ flex: 1 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/quizzes" element={<AllQuizzes />} />
              <Route path="/quizzes/:id" element={<QuizDetail />} />
              <Route path="/quizzes/:id/take" element={
                <PrivateRoute><TakeQuiz /></PrivateRoute>
              } />
              <Route path="/quizzes/:id/results" element={
                <PrivateRoute><Results /></PrivateRoute>
              } />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/teacher" element={
                <TeacherRoute><TeacherDashboard /></TeacherRoute>
              } />
              <Route path="/teacher/create" element={
                <TeacherRoute><CreateQuiz /></TeacherRoute>
              } />
              <Route path="/teacher/edit/:id" element={
                <TeacherRoute><CreateQuiz /></TeacherRoute>
              } />
              <Route path="/profile" element={
                <PrivateRoute><Profile /></PrivateRoute>
              } />
              <Route path="*" element={<NotFound />} />
              <Route path="/404" element={<NotFound />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </BrowserRouter>
    </ThemeProvider>
  );
}