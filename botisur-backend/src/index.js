// src/index.js
import app from './app.js';

const main = () => {
    app.listen(app.get('port'), () => {
        console.log(`✅ Servidor corriendo en el puerto ${app.get('port')}`);
    });
};

main();