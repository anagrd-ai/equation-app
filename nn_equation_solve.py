import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import math

# Generate training data
def generate_data(num_points: int, bounds: float):
    x = np.random.uniform(-bounds, bounds, num_points)
    y = np.random.uniform(-bounds, bounds, num_points)
    z = np.cos(np.sqrt(x * x + y * y))
    # z = np.cos(x * y)
    return x, y, z

# Create the neural network model
def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(2,)),  # Use Input layer
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Train the model
def train_model(model, x_train, y_train, z_train, epochs=14):
    history = model.fit(
        np.column_stack((x_train, y_train)),
        z_train,
        epochs=epochs,
        validation_split=0.2,
        verbose=0
    )
    return history

# Plot the results
def plot_results_png(x_test, y_test, z_test, z_pred):
    fig = plt.figure(figsize=(16, 8))

    ax1 = fig.add_subplot(121, projection='3d')
    ax1.scatter(x_test, y_test, z_test, c='b', marker=".", label='True')
    ax1.set_title('True Function')

    ax2 = fig.add_subplot(122, projection='3d')
    ax2.scatter(x_test, y_test, z_pred, c='r', marker=".", label='Predicted')
    ax2.set_title('Predicted Function')

    for ax in [ax1, ax2]:
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

    plt.tight_layout()
    # plt.show()
    plt.savefig('my_plot.png')

# Main function
def main():
    print(f"TensorFlow version {tf.__version__}")
    print(f"TensorFlow devices {tf.config.list_physical_devices()}\n")

    # Generate data
    x_train, y_train, z_train = generate_data(14400, math.pi * 2.0)
    x_test, y_test, z_test = generate_data(6400, math.pi * 2.0)

    # Create and train the model
    model = create_model()
    history = train_model(model, x_train, y_train, z_train)

    # Make predictions
    z_pred = model.predict(np.column_stack((x_test, y_test))).flatten()

    # Plot the results
    plot_results_png(x_test, y_test, z_test, z_pred)

    # Print the mean squared error
    mse = np.mean((z_test - z_pred)**2)
    print(f"Mean Squared Error: {mse}")

if __name__ == "__main__":
    main()
