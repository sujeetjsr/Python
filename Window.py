import cv2

# Create a blank window
cv2.namedWindow("Simple Window", cv2.WINDOW_NORMAL)

# Display the window until 'q' is pressed
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
