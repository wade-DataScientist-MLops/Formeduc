import React from 'react';
import styled from 'styled-components';
import { Message } from '../../types';

const MessageRow = styled.div<{ isUser: boolean }>`
  display: flex;
  width: 100%;
  margin-bottom: 12px;
  justify-content: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  /* INVERSION: isUser=true → droite (utilisateur), isUser=false → gauche (assistant) */
`;

const MessageContainer = styled.div<{ isUser: boolean }>`
  border-radius: 20px;
  padding: 15px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  max-width: 80%;
  word-wrap: break-word;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  line-height: 1.4;
  background-color: ${props => props.isUser ? '#dcfce7' : '#e1f0ff'};
  border-bottom-right-radius: ${props => props.isUser ? '5px' : '20px'};
  border-bottom-left-radius: ${props => props.isUser ? '20px' : '5px'};
  flex-direction: ${props => props.isUser ? 'row-reverse' : 'row'};
`;

const Avatar = styled.div<{ isUser: boolean; isElavira?: boolean; isSolenys?: boolean }>`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2em;
  font-weight: bold;
  color: white;
  background-color: ${props => {
    if (props.isUser) return '#3b82f6';
    if (props.isElavira) return '#88c0d0';
    if (props.isSolenys) return '#f093fb';
    return '#ccc';
  }};
  border: 2px solid #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
`;

const AvatarImage = styled.img`
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
`;

const AvatarInitial = styled.div`
  font-size: 1.2em;
  font-weight: bold;
  color: white;
`;

const MessageContent = styled.div`
  flex-grow: 1;
`;

const MessageHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
`;

const UserName = styled.strong`
  font-weight: 700;
  color: #2c3e50;
`;

const Timestamp = styled.span`
  font-size: 0.8em;
  color: #777;
`;

const MessageText = styled.div`
  color: #2c3e50;
  white-space: pre-wrap;
`;

const AudioPlayer = styled.audio`
  margin-top: 10px;
  width: 100%;
`;

const getAvatarContent = (message: Message) => {
  if (message.user_id === 'Elavira Assistant') {
    return 'E';
  } else if (message.user_id === 'Solenys Assistant') {
    return 'S';
  } else {
    return message.user_id.charAt(0).toUpperCase();
  }
};

const getAvatarImage = (message: Message) => {
  if (message.user_id === 'Elavira Assistant') {
    return '/images/elavira-real.png';
  } else if (message.user_id === 'Solenys Assistant') {
    return '/images/solenys-banner.svg';
  }
  return null;
};

const formatTimestamp = (timestamp: string) => {
  try {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('fr-FR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  } catch {
    return timestamp.slice(11, 16) || timestamp;
  }
};

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  // Detection FORCÉE des messages d'assistant
  const isElavira = message.user_id === 'Elavira Assistant' || message.user_id === 'Elavira';
  const isSolenys = message.user_id === 'Solenys Assistant' || message.user_id === 'Solenys';
  const isAssistant = isElavira || isSolenys || message.user_id.includes('Assistant') || message.user_id.includes('Solenys') || message.user_id.includes('Elavira');
  
  // CORRECTION: assistants à droite, utilisateurs à gauche
  const isUser = !isAssistant;
  
  // Debug pour vérifier la détection
  console.log(`[MessageBubble] user_id: "${message.user_id}", isElavira: ${isElavira}, isSolenys: ${isSolenys}, isAssistant: ${isAssistant}, isUser: ${isUser}`);
  console.log(`[MessageBubble] Alignement: ${isUser ? 'DROITE (utilisateur)' : 'GAUCHE (assistant)'}`);
  
  // INVERSION: isUser=true → Droite (utilisateur), isUser=false → Gauche (assistant)




  return (
    <MessageRow isUser={isUser}>
      <MessageContainer isUser={isUser}>
        <Avatar 
          isUser={isUser} 
          isElavira={isElavira} 
          isSolenys={isSolenys}
        >
          {(() => {
            const avatarImage = getAvatarImage(message);
            return avatarImage ? (
              <AvatarImage 
                src={avatarImage} 
                alt={message.user_id}
                onError={(e) => {
                  // Fallback vers l'initiale si l'image ne charge pas
                  const target = e.target as HTMLImageElement;
                  target.style.display = 'none';
                  const parent = target.parentElement;
                  if (parent) {
                    parent.innerHTML = getAvatarContent(message);
                  }
                }}
              />
            ) : (
              <AvatarInitial>{getAvatarContent(message)}</AvatarInitial>
            );
          })()}
        </Avatar>
        
        <MessageContent>
          <MessageHeader>
            <UserName>{message.user_id}</UserName>
            <Timestamp>({formatTimestamp(message.timestamp)})</Timestamp>
          </MessageHeader>
          <MessageText>{message.text}</MessageText>
          
          {message.audio_base64 && (
            <AudioPlayer controls>
              <source 
                src={`data:audio/mp3;base64,${message.audio_base64}`} 
                type="audio/mp3" 
              />
              Votre navigateur ne supporte pas l'élément audio.
            </AudioPlayer>
          )}
        </MessageContent>
      </MessageContainer>
    </MessageRow>
  );
};

