import React, { useState, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import { motion } from 'framer-motion';
import { AnimatedImageComponent } from '../AnimatedImage/AnimatedImage';

const slideIn = keyframes`
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
`;

const slideOut = keyframes`
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(-100%);
    opacity: 0;
  }
`;

const CarouselContainer = styled.div`
  position: relative;
  width: 100%;
  height: 400px;
  overflow: hidden;
  border-radius: 25px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
  margin: 20px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  perspective: 1000px;
`;

const CarouselTrack = styled(motion.div)<{ translateX: number }>`
  display: flex;
  width: 100%;
  height: 100%;
  transform: translateX(${props => props.translateX}px);
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
`;

const CarouselItem = styled(motion.div)<{ isActive: boolean }>`
  min-width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  animation: ${props => props.isActive ? slideIn : slideOut} 0.6s ease-in-out;
`;

const ImageContainer = styled.div`
  width: 100%;
  height: 100%;
  position: relative;
`;

const ImageOverlay = styled(motion.div)`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    45deg,
    rgba(0, 0, 0, 0.6) 0%,
    rgba(0, 0, 0, 0.2) 50%,
    rgba(0, 0, 0, 0.05) 100%
  );
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
  padding: 30px;
  backdrop-filter: blur(2px);
  border-radius: 25px;
`;

const AssistantName = styled(motion.h2)`
  font-size: 2.8rem;
  font-weight: 700;
  margin-bottom: 15px;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  background-size: 200% 200%;
  animation: gradientShift 3s ease-in-out infinite;
  
  @keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
  }
`;

const AssistantDescription = styled(motion.p)`
  font-size: 1.3rem;
  font-weight: 500;
  margin-bottom: 20px;
  text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.7);
  max-width: 85%;
  line-height: 1.5;
`;

const AssistantFeatures = styled(motion.div)`
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
  justify-content: center;
`;

const FeatureTag = styled(motion.span)`
  background: rgba(255, 255, 255, 0.25);
  padding: 10px 18px;
  border-radius: 25px;
  font-size: 0.95rem;
  font-weight: 600;
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.4);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
`;

const NavigationDots = styled.div`
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 10;
`;

const Dot = styled.button<{ isActive: boolean }>`
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: none;
  background: ${props => props.isActive ? 'white' : 'rgba(255, 255, 255, 0.5)'};
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: white;
    transform: scale(1.2);
  }
`;

const NavigationArrows = styled.div`
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
`;

const ArrowButton = styled.button`
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  
  &:hover {
    background: rgba(0, 0, 0, 0.8);
    transform: translateY(-50%) scale(1.1);
  }
  
  &:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }
`;

const LeftArrow = styled(ArrowButton)`
  left: 20px;
`;

const RightArrow = styled(ArrowButton)`
  right: 20px;
`;

interface CarouselItemData {
  id: string;
  image: string;
  name: string;
  description: string;
  features: string[];
}

interface ImageCarouselProps {
  items: CarouselItemData[];
  autoPlay?: boolean;
  autoPlayInterval?: number;
}

export const ImageCarousel: React.FC<ImageCarouselProps> = ({
  items,
  autoPlay = true,
  autoPlayInterval = 5000
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);

  useEffect(() => {
    if (!autoPlay || items.length <= 1) return;

    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % items.length);
    }, autoPlayInterval);

    return () => clearInterval(interval);
  }, [autoPlay, autoPlayInterval, items.length]);

  const goToSlide = (index: number) => {
    if (isTransitioning || index === currentIndex) return;
    
    setIsTransitioning(true);
    setCurrentIndex(index);
    
    setTimeout(() => {
      setIsTransitioning(false);
    }, 500);
  };

  const goToPrevious = () => {
    if (isTransitioning) return;
    const newIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
    goToSlide(newIndex);
  };

  const goToNext = () => {
    if (isTransitioning) return;
    const newIndex = (currentIndex + 1) % items.length;
    goToSlide(newIndex);
  };

  if (items.length === 0) return null;

  return (
    <CarouselContainer>
      <CarouselTrack 
        translateX={-currentIndex * 100}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        {items.map((item, index) => (
          <CarouselItem 
            key={item.id} 
            isActive={index === currentIndex}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ 
              scale: index === currentIndex ? 1 : 0.9, 
              opacity: 1 
            }}
            transition={{ 
              duration: 0.6, 
              ease: "easeOut" 
            }}
          >
            <ImageContainer>
              <AnimatedImageComponent
                src={item.image}
                alt={item.name}
                onClick={() => goToSlide(index)}
              />
            </ImageContainer>
            <ImageOverlay
              initial={{ opacity: 0, y: 20 }}
              animate={{ 
                opacity: index === currentIndex ? 1 : 0.7, 
                y: 0 
              }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              <AssistantName
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                {item.name}
              </AssistantName>
              <AssistantDescription
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                {item.description}
              </AssistantDescription>
              <AssistantFeatures
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.5 }}
              >
                {item.features.map((feature, featureIndex) => (
                  <FeatureTag 
                    key={featureIndex}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ 
                      duration: 0.4, 
                      delay: 0.6 + featureIndex * 0.1 
                    }}
                    whileHover={{ 
                      scale: 1.05, 
                      backgroundColor: "rgba(255, 255, 255, 0.4)" 
                    }}
                  >
                    {feature}
                  </FeatureTag>
                ))}
              </AssistantFeatures>
            </ImageOverlay>
          </CarouselItem>
        ))}
      </CarouselTrack>

      {items.length > 1 && (
        <>
          <NavigationArrows>
            <LeftArrow onClick={goToPrevious} disabled={isTransitioning}>
              ‹
            </LeftArrow>
            <RightArrow onClick={goToNext} disabled={isTransitioning}>
              ›
            </RightArrow>
          </NavigationArrows>

          <NavigationDots>
            {items.map((_, index) => (
              <Dot
                key={index}
                isActive={index === currentIndex}
                onClick={() => goToSlide(index)}
              />
            ))}
          </NavigationDots>
        </>
      )}
    </CarouselContainer>
  );
};
