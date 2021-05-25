
import cv2 
import numpy as np

class SavModel:

    def relu_activation(self,data):
        return np.maximum(data,0)

    def softmax(self,A):
        expA = np.exp(A)
        return expA / expA.sum(axis=1, keepdims=True)

    def cross_entropy_softmax_loss_array(self,softmax_probs_array, y_onehot):
        indices = np.argmax(y_onehot, axis = 1).astype(int)
        predicted_probability = softmax_probs_array[np.arange(len(softmax_probs_array)), indices]
        log_preds = np.log(predicted_probability)
        loss = -1.0 * np.sum(log_preds) / len(log_preds)
        return loss

    def regularization_L2_softmax_loss(self,reg_lambda, weight1, weight2):
        weight1_loss = 0.5 * reg_lambda * np.sum(weight1 * weight1)
        weight2_loss = 0.5 * reg_lambda * np.sum(weight2 * weight2)
        return weight1_loss + weight2_loss

        
    def Predict(self,x_test):
        
        input_layer = np.dot(x_test, self.layer1_weights_array)
        hidden_layer = self.relu_activation(input_layer + self.layer1_biases_array)
        scores = np.dot(hidden_layer, self.layer2_weights_array) + self.layer2_biases_array
        probs = self.softmax(scores)
        
        y_pred=np.argmax(probs, axis = 1)
        
        return y_pred

    def Train(self,x,y):
        
        training_data=x
        training_labels=y

        hidden_nodes = 11
        num_features = training_data.shape[1]
        num_labels = training_labels.shape[1]

        self.layer1_weights_array = np.random.randn(num_features, hidden_nodes) 
        self.layer1_biases_array = np.zeros((1, hidden_nodes))

        self.layer2_weights_array = np.random.randn(hidden_nodes, num_labels) 
        self.layer2_biases_array = np.zeros((1, num_labels))

        learning_rate = 0.5
        reg_lambda = 0.01
        
        for step in range(50):

            input_layer = np.dot(training_data, self.layer1_weights_array)
            hidden_layer = self.relu_activation(input_layer + self.layer1_biases_array)
            output_layer = np.dot(hidden_layer, self.layer2_weights_array) + self.layer2_biases_array
            output_probs = self.softmax(output_layer)

            loss = self.cross_entropy_softmax_loss_array(output_probs, training_labels)
            loss += self.regularization_L2_softmax_loss(reg_lambda, self.layer1_weights_array, self.layer2_weights_array)

            output_error_signal = (output_probs - training_labels) / output_probs.shape[0]

            error_signal_hidden = np.dot(output_error_signal, self.layer2_weights_array.T) 
            error_signal_hidden[hidden_layer <= 0] = 0

            gradient_layer2_weights = np.dot(hidden_layer.T, output_error_signal)
            gradient_layer2_bias = np.sum(output_error_signal, axis = 0, keepdims = True)

            gradient_layer1_weights = np.dot(training_data.T, error_signal_hidden)
            gradient_layer1_bias = np.sum(error_signal_hidden, axis = 0, keepdims = True)

            gradient_layer2_weights += reg_lambda * self.layer2_weights_array
            gradient_layer1_weights += reg_lambda * self.layer1_weights_array

            self.layer1_weights_array -= learning_rate * gradient_layer1_weights
            self.layer1_biases_array -= learning_rate * gradient_layer1_bias
            self.layer2_weights_array -= learning_rate * gradient_layer2_weights
            self.layer2_biases_array -= learning_rate * gradient_layer2_bias

            if step % 30 == 0:
                    print ('Loss at step {0}: {1}'.format(step, loss))