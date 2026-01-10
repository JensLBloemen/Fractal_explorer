from App.app import App

def f(z):
    return z ** 2

if __name__ == "__main__":
    app = App([-2, 2], [-3, 3], f)
    app.run()