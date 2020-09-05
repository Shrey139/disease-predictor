import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import GUI as gui

data = pd.read_csv('Database/Training.csv')

print(data)

df = pd.DataFrame(data)

cols = df.columns[:-1]

x = df[cols]  # x is the feature
y = df['prognosis']  # y is the target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

dt = DecisionTreeClassifier()

dt.fit(x_train, y_train)

# score = dt.score(x_test, y_test)

# print(f"Accuracy: {score * 100}%")

features = cols
feature_dict = {}

for i, f in enumerate(features):
    feature_dict[f] = i

latest_features = list(features).copy()

trix = dict()

for item in latest_features:
    trix[str(item).title().replace('_', ' ')] = item


def prediction():
    # symptoms = ['joint_pain', 'muscle_wasting']
    symptoms = [gui.p.get(), gui.en.get(), gui.bb.get(), gui.ee.get(),
                gui.hh.get()]
    symptoms = [trix[j] for j in symptoms if j != '']

    hack_set = set()

    pos = []

    for i in range(len(symptoms)):
        pos.append(feature_dict[symptoms[i]])

    sample_x = [1.0 if i in pos else 0.0 for i in range(len(features))]
    sample_x = [sample_x]  # np.array(sample_x).reshape(1, len(sample_x))

    # print(sample_x)

    # Decision Tree

    dt = DecisionTreeClassifier()

    dt.fit(x_train, y_train)

    print(dt.predict(sample_x))

    hack_set.add(*map(str, dt.predict(sample_x)))

    # score = dt.score(x_test, y_test)

    # print(f"Accuracy: {score * 100}%")

    # Naive Bayes

    naive = GaussianNB()

    naive.fit(x_train, y_train)

    hack_set.add(*map(str, naive.predict(sample_x)))

    score = naive.score(x_test, y_test)

    print(f"Accuracy: {score * 100}%")

    magic = list(hack_set)

    s = ""

    if len(hack_set) == 1:
        s = s + "".join(magic[0])
    else:
        s = s + "".join(magic[0]) + ' or ' + "".join(magic[1])

    # Exceptions for Wrong Try
    if not symptoms:
        gui.final_result.delete(0, gui.END)
        gui.final_result.insert(0, "Invalid ! No Disease Found")

    elif len(set(symptoms)) != len(symptoms):
        gui.final_result.delete(0, gui.END)
        gui.final_result.insert(0, "Invalid ! Try with unique Symptoms")
    else:
        gui.final_result.delete(0, gui.END)
        gui.final_result.insert(0, s)
