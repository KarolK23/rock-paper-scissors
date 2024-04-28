from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

def player(prev_play, opponent_history=[]):
    guess = "S"
    opponent_history.append(prev_play)

    if len(opponent_history) == 1000:
        opponent_history.clear()

    if len(opponent_history)>5:
        pre_prev_move3 = opponent_history[0:-4]
        pre_prev_move2 = opponent_history[1:-3]
        pre_prev_move = opponent_history[2:-2]
        prev_move = opponent_history[3:-1]
        next_move = opponent_history[4::]
        history = pd.DataFrame({
            'pre_prev_move3': pre_prev_move3,
            'pre_prev_move2': pre_prev_move2,
            'pre_prev_move': pre_prev_move,
            'prev_move': prev_move, 
            'next_move': next_move})

        mapping = {'P': 0, 'R': 1, 'S': 2}

        history['pre_prev_move3'] = history['pre_prev_move3'].map(mapping)
        history['pre_prev_move2'] = history['pre_prev_move2'].map(mapping)
        history['pre_prev_move'] = history['pre_prev_move'].map(mapping)
        history['prev_move'] = history['prev_move'].map(mapping)
        history['next_move'] = history['next_move'].map(mapping)
        history.fillna(0, inplace=True)
        
        model = DecisionTreeClassifier(random_state = 42)
        model.fit(history[['pre_prev_move3', 'pre_prev_move2', 'pre_prev_move','prev_move']], history['next_move'])

        prev_move = pd.DataFrame({
            'pre_prev_move3': opponent_history[-4],
            'pre_prev_move2': opponent_history[-3], 
            'pre_prev_move': opponent_history[-2], 
            'prev_move': opponent_history[-1]}, 
            index=[0])
        
        prev_move['pre_prev_move3'] = prev_move['pre_prev_move3'].map(mapping)
        prev_move['pre_prev_move2'] = prev_move['pre_prev_move2'].map(mapping)
        prev_move['pre_prev_move'] = prev_move['pre_prev_move'].map(mapping)
        prev_move['prev_move'] = prev_move['prev_move'].map(mapping)
        next_move_pred = model.predict(prev_move)

        reverse_mapping = {v: k for k, v in mapping.items()}

        predicted_move = next_move_pred[0]

        predicted_move_letter = reverse_mapping[predicted_move]

        if predicted_move_letter == "R":
            guess = "P"
        elif predicted_move_letter == "P":
            guess = "S"
        elif predicted_move_letter == "S":
            guess = "R"
        

    return guess
