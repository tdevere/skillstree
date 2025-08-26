import express from 'express';
import bodyParser from 'body-parser';
import { createConnection } from './db';
import routes from './routes';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

createConnection();

routes(app);

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});