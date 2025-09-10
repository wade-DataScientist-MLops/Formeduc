import React, { useState } from 'react';
import styled from 'styled-components';
import { useApp } from '../../context/AppContext';
import { authAPI } from '../../services/api';

const AuthContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
`;

const AuthCard = styled.div`
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
`;

const Title = styled.h1`
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  font-weight: 600;
`;

const Subtitle = styled.h2`
  color: #34495e;
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.2rem;
  font-weight: 500;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const Input = styled.input`
  padding: 15px 20px;
  border: 2px solid #e1e8ed;
  border-radius: 25px;
  font-size: 16px;
  transition: all 0.3s ease;
  background-color: #f8f9fa;

  &:focus {
    outline: none;
    border-color: #3b82f6;
    background-color: white;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }

  &::placeholder {
    color: #a0aec0;
  }
`;

const Button = styled.button`
  padding: 15px 30px;
  background: linear-gradient(135deg, #3b82f6, #2e6bb4);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(59, 130, 246, 0.3);
  }

  &:disabled {
    background: #a0a0a0;
    cursor: not-allowed;
    transform: none;
  }
`;

const SecondaryButton = styled.button`
  padding: 12px 25px;
  background: transparent;
  color: #3b82f6;
  border: 2px solid #3b82f6;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 10px;

  &:hover {
    background: #3b82f6;
    color: white;
  }
`;

const ErrorMessage = styled.div`
  background: #fed7d7;
  color: #c53030;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 14px;
  margin-bottom: 15px;
`;

const SuccessMessage = styled.div`
  background: #c6f6d5;
  color: #2f855a;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 14px;
  margin-bottom: 15px;
`;

const Divider = styled.div`
  text-align: center;
  margin: 20px 0;
  color: #a0aec0;
  font-size: 14px;
`;

const ExpandableSection = styled.div<{ expanded: boolean }>`
  max-height: ${props => props.expanded ? '300px' : '0'};
  overflow: hidden;
  transition: max-height 0.3s ease;
`;

const ToggleButton = styled.button`
  background: none;
  border: none;
  color: #3b82f6;
  cursor: pointer;
  font-size: 14px;
  text-decoration: underline;
  margin: 10px 0;
`;

export const AuthForm: React.FC = () => {
  const { dispatch } = useApp();
  const [isLogin, setIsLogin] = useState(true);
  const [isRegisterExpanded, setIsRegisterExpanded] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError('');
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await authAPI.login(formData.username, formData.password);
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('logged_in_user', formData.username);
      
      dispatch({ type: 'SET_ACCESS_TOKEN', payload: response.access_token });
      dispatch({ type: 'SET_LOGGED_IN_USER', payload: formData.username });
      dispatch({ type: 'SET_PAGE', payload: 'chat' });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      setLoading(false);
      return;
    }

    try {
      await authAPI.register(formData.username, formData.password);
      setSuccess('Compte créé avec succès ! Vous pouvez maintenant vous connecter.');
      setIsLogin(true);
      setFormData({ username: formData.username, password: '', confirmPassword: '' });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Erreur lors de la création du compte');
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthContainer>
      <AuthCard>
        <Title>Bienvenue sur Elavira 👋</Title>
        
        {isLogin ? (
          <>
            <Subtitle>Connectez-vous</Subtitle>
            <Form onSubmit={handleLogin}>
              {error && <ErrorMessage>{error}</ErrorMessage>}
              {success && <SuccessMessage>{success}</SuccessMessage>}
              
              <Input
                type="text"
                name="username"
                placeholder="Votre nom d'utilisateur"
                value={formData.username}
                onChange={handleInputChange}
                required
              />
              <Input
                type="password"
                name="password"
                placeholder="Votre mot de passe"
                value={formData.password}
                onChange={handleInputChange}
                required
              />
              <Button type="submit" disabled={loading}>
                {loading ? 'Connexion...' : 'Se connecter'}
              </Button>
            </Form>

            <Divider>Nouvel utilisateur ?</Divider>
            <div style={{ textAlign: 'center' }}>
              <p style={{ color: '#a0aec0', marginBottom: '10px' }}>
                Créez un compte pour accéder à toutes les fonctionnalités.
              </p>
              <ToggleButton onClick={() => setIsRegisterExpanded(!isRegisterExpanded)}>
                {isRegisterExpanded ? 'Masquer' : 'S\'inscrire'}
              </ToggleButton>
            </div>

            <ExpandableSection expanded={isRegisterExpanded}>
              <Form onSubmit={handleRegister}>
                <Input
                  type="text"
                  name="username"
                  placeholder="Nouveau nom d'utilisateur"
                  value={formData.username}
                  onChange={handleInputChange}
                  required
                />
                <Input
                  type="password"
                  name="password"
                  placeholder="Nouveau mot de passe"
                  value={formData.password}
                  onChange={handleInputChange}
                  required
                />
                <Input
                  type="password"
                  name="confirmPassword"
                  placeholder="Confirmer le mot de passe"
                  value={formData.confirmPassword}
                  onChange={handleInputChange}
                  required
                />
                <Button type="submit" disabled={loading}>
                  {loading ? 'Création...' : 'Créer mon compte'}
                </Button>
              </Form>
            </ExpandableSection>
          </>
        ) : (
          <>
            <Subtitle>Créer un compte</Subtitle>
            <Form onSubmit={handleRegister}>
              {error && <ErrorMessage>{error}</ErrorMessage>}
              {success && <SuccessMessage>{success}</SuccessMessage>}
              
              <Input
                type="text"
                name="username"
                placeholder="Nouveau nom d'utilisateur"
                value={formData.username}
                onChange={handleInputChange}
                required
              />
              <Input
                type="password"
                name="password"
                placeholder="Nouveau mot de passe"
                value={formData.password}
                onChange={handleInputChange}
                required
              />
              <Input
                type="password"
                name="confirmPassword"
                placeholder="Confirmer le mot de passe"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                required
              />
              <Button type="submit" disabled={loading}>
                {loading ? 'Création...' : 'Créer mon compte'}
              </Button>
            </Form>

            <Divider>Déjà un compte ?</Divider>
            <SecondaryButton onClick={() => setIsLogin(true)}>
              Se connecter
            </SecondaryButton>
          </>
        )}
      </AuthCard>
    </AuthContainer>
  );
};
