import React, { useState } from 'react';
import styled, { keyframes } from 'styled-components';
import { motion } from 'framer-motion';

// Animation de respiration subtile (pour usage futur)
// const breathe = keyframes`
//   0%, 100% { transform: scale(1) translateY(0px); }
//   50% { transform: scale(1.02) translateY(-2px); }
// `;

// Animation de clignotement des yeux (pour usage futur)
// const blink = keyframes`
//   0%, 90%, 100% { opacity: 1; }
//   95% { opacity: 0.3; }
// `;

// Animation de pulsation de l'aura
const auraPulse = keyframes`
  0%, 100% { 
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.3), 0 0 40px rgba(59, 130, 246, 0.1);
    transform: scale(1);
  }
  50% { 
    box-shadow: 0 0 30px rgba(59, 130, 246, 0.5), 0 0 60px rgba(59, 130, 246, 0.2);
    transform: scale(1.05);
  }
`;

const ImageContainer = styled(motion.div)`
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  
  &:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  }
`;

const ImageWrapper = styled.div`
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 20px;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
`;

const PlaceholderContent = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
  padding: 20px;
`;

const PlaceholderIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 10px;
  opacity: 0.8;
`;

const PlaceholderText = styled.div`
  font-size: 1.2rem;
  font-weight: 600;
  opacity: 0.9;
`;

// Image animée remplacée par motion.img
// const AnimatedImage = styled.img`
//   width: 100%;
//   height: 100%;
//   object-fit: cover;
//   border-radius: 20px;
//   animation: ${breathe} 4s ease-in-out infinite;
//   transition: all 0.3s ease;
//   
//   ${ImageContainer}:hover & {
//     animation: ${breathe} 2s ease-in-out infinite;
//     filter: brightness(1.1) contrast(1.05);
//   }
// `;

const AuraEffect = styled.div`
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
  border-radius: 30px;
  background: linear-gradient(45deg, 
    rgba(59, 130, 246, 0.1) 0%, 
    rgba(147, 51, 234, 0.1) 50%, 
    rgba(236, 72, 153, 0.1) 100%
  );
  animation: ${auraPulse} 3s ease-in-out infinite;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
  
  ${ImageContainer}:hover & {
    opacity: 1;
  }
`;

const FloatingElements = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
`;

const FloatingDot = styled.div<{ delay: number; duration: number; size: number }>`
  position: absolute;
  width: ${props => props.size}px;
  height: ${props => props.size}px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, transparent 70%);
  border-radius: 50%;
  animation: float ${props => props.duration}s ease-in-out infinite;
  animation-delay: ${props => props.delay}s;
  opacity: 0;
  transition: opacity 0.3s ease;
  
  ${ImageContainer}:hover & {
    opacity: 1;
  }
  
  @keyframes float {
    0%, 100% { 
      transform: translateY(0px) translateX(0px) scale(0.8);
      opacity: 0;
    }
    50% { 
      transform: translateY(-20px) translateX(10px) scale(1);
      opacity: 0.6;
    }
  }
`;

const GlowEffect = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: ${auraPulse} 4s ease-in-out infinite;
  z-index: -1;
  opacity: 0;
  transition: opacity 0.3s ease;
  
  ${ImageContainer}:hover & {
    opacity: 1;
  }
`;

interface AnimatedImageProps {
  src: string;
  alt: string;
  onClick?: () => void;
  className?: string;
}

export const AnimatedImageComponent: React.FC<AnimatedImageProps> = ({ 
  src, 
  alt, 
  onClick, 
  className 
}) => {
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);

  const containerVariants = {
    initial: { scale: 1, rotateY: 0 },
    hover: { 
      scale: 1.05, 
      rotateY: 5
    }
  };

  const imageVariants = {
    initial: { scale: 1, filter: "brightness(1)" },
    hover: { 
      scale: 1.02, 
      filter: "brightness(1.1) contrast(1.05)"
    }
  };

  return (
    <ImageContainer
      variants={containerVariants}
      initial="initial"
      whileHover="hover"
      transition={{ 
        type: "spring", 
        stiffness: 300, 
        damping: 20 
      }}
      onClick={onClick}
      className={className}
    >
      <ImageWrapper>
        {!imageError ? (
          <motion.img
            src={src}
            alt={alt}
            variants={imageVariants}
            initial="initial"
            whileHover="hover"
            transition={{ 
              type: "spring", 
              stiffness: 400, 
              damping: 25 
            }}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              borderRadius: '20px',
              opacity: imageLoaded ? 1 : 0,
              transition: 'opacity 0.3s ease'
            }}
            onLoad={() => setImageLoaded(true)}
            onError={() => {
              console.log('Image failed to load:', src);
              setImageError(true);
            }}
          />
        ) : null}
        
        {(!imageLoaded && !imageError) && (
          <PlaceholderContent>
            <PlaceholderIcon>⏳</PlaceholderIcon>
            <PlaceholderText>Chargement...</PlaceholderText>
          </PlaceholderContent>
        )}
        
        {imageError && (
          <PlaceholderContent>
            <PlaceholderIcon>🤖</PlaceholderIcon>
            <PlaceholderText>{alt}</PlaceholderText>
          </PlaceholderContent>
        )}
        
        <AuraEffect />
        <GlowEffect />
        
        <FloatingElements>
          <FloatingDot 
            delay={0} 
            duration={3} 
            size={4}
            style={{ top: '20%', left: '15%' }}
          />
          <FloatingDot 
            delay={1} 
            duration={4} 
            size={6}
            style={{ top: '60%', right: '20%' }}
          />
          <FloatingDot 
            delay={2} 
            duration={5} 
            size={3}
            style={{ bottom: '30%', left: '25%' }}
          />
          <FloatingDot 
            delay={0.5} 
            duration={3.5} 
            size={5}
            style={{ top: '40%', right: '10%' }}
          />
        </FloatingElements>
      </ImageWrapper>
    </ImageContainer>
  );
};
