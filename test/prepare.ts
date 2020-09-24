import chai from 'chai';
import chaiAsPromised from 'chai-as-promised';
import mochaPrepare from 'mocha-prepare';

mochaPrepare(
  (done) => {
    chai.use(chaiAsPromised);
    done();
  },
  (done) => {
    done();
  },
);
