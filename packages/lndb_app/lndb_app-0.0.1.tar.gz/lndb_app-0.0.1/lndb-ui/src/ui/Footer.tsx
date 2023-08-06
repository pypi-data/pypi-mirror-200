import { footerHeight } from '../utils/constants';

export const Footer = () => {
  return (
    <div>
      <hr
        aria-orientation="horizontal"
        className="chakra-divider css-svjswr"
      ></hr>{' '}
      {/* divider */}
      <div style={{ height: footerHeight, padding: '1%' }}>
        <div className="container-fluid">
          <div className="row">
            <div className="col-sm">
              <h6
                className="text-bold"
                style={{ fontWeight: 'bold', padding: '1.5rem 0 1.05rem' }}
              >
                Documentation
              </h6>
              <ul className="list-unstyled mb-0">
                <li>
                  <a href="https://lamin.ai/docs/db">LaminDB</a>
                </li>
                <li>
                  <a href="https://lamin.ai/docs/bionty">Bionty</a>
                </li>
                <li>
                  <a href="https://lamin.ai/docs/nbproject">nbproject</a>
                </li>
              </ul>
            </div>
            <div className="col-sm">
              <h6
                className="text-bold"
                style={{ fontWeight: 'bold', padding: '1.5rem 0 1.05rem' }}
              >
                Social
              </h6>
              <ul className="list-unstyled">
                <li>
                  <a href="https://twitter.com/laminlabs">Twitter</a>
                </li>
                <li>
                  <a href="https://github.com/laminlabs">GitHub</a>
                </li>
                <li>
                  <a href="https://linkedin.com/company/lamin-labs">LinkedIn</a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="text-center" style={{ marginTop: '1.5rem' }}>
          <small>
            Made with 🤔 & ❤️ worldwide, HQ Munich.
            <br />© 2023 Lamin Labs ·{' '}
            <a href="https://lamin.ai/imprint">Imprint</a> ·{' '}
            <a href="https://lamin.ai/contact">Contact</a>
          </small>
        </div>
      </div>
    </div>
  );
};
