import { createConnection } from 'typeorm';

import ormconfig from './ormconfig';
import { createServer } from './server';

(async () => {
  await createConnection(ormconfig);

  const server = createServer();
  server.listen(process.env.PORT || '8080');
})();
