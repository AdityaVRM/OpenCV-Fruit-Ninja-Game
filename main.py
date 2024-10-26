import cv2
import mediapipe as mp
import pygame
import random

# Initialize MediaPipe for hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Fruit Ninja Clone - Circles Edition")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


# Circle Class to manage the circles (fruits)
class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 30
        self.speed = random.randint(5, 10)
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])  # Random colors

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


# Circle list
circles = [Circle(random.randint(50, 750), random.randint(-300, -50)) for _ in range(5)]

# Video Capture for hand tracking
cap = cv2.VideoCapture(0)

# Game Loop
running = True
score = 0

while running:
    # Clear the screen
    screen.fill(WHITE)

    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)  # Mirror the frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Draw circles and move them downwards
    for circle in circles:
        circle.move()
        circle.draw()

        # Reset circle position if it goes off screen
        if circle.y > 600:
            circle.x = random.randint(50, 750)
            circle.y = random.randint(-300, -50)
            circle.speed = random.randint(5, 10)

    # Check for slicing gesture and collisions
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get coordinates of the index finger tip
            x, y = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * 800), \
                int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * 600)

            # Draw a circle at the index finger tip (for visualization)
            pygame.draw.circle(screen, GREEN, (x, y), 10)

            # Detect collision with circles
            for circle in circles:
                distance = ((circle.x - x) ** 2 + (circle.y - y) ** 2) ** 0.5
                if distance < circle.radius + 10:  # Check if the fingertip is touching the circle
                    circles.remove(circle)
                    score += 1
                    # Add a new circle to maintain the number of circles
                    circles.append(Circle(random.randint(50, 750), random.randint(-300, -50)))

    # Render the score on the screen
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Event handling for exiting the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the Pygame display
    pygame.display.flip()
    clock.tick(30)

# Release resources
cap.release()
pygame.quit()
cv2.destroyAllWindows()