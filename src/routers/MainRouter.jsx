import React from 'react';
import { Routes, Route, useLocation } from 'react-router-dom';
import {
  CSSTransition,
  TransitionGroup,
} from 'react-transition-group';

import Home from '../pages/home';
// import LoginUser from '../pages/loginUser';
// import UserSignUp from '../pages/userSignUp';

function MainRouter() {
  const location = useLocation();

  React.useLayoutEffect(() => {
    window.scrollTo(0, 0);
  }, [location.pathname]);

  return (
    <TransitionGroup>
      <CSSTransition
        key={window.location.href}
        timeout={1000}
        classNames="fade"
      >
        <Routes>
          <Route path="/" element={<Home />} />
          {/* <Route path="/userSignUp" element={<UserSignUp />} />
          <Route path="/userLogin" element={<LoginUser />} /> */}
          {/* <Route path="/hrLogin" element={<HRLogin />} /> */}
        </Routes>
      </CSSTransition>
    </TransitionGroup>
  );
}

export default MainRouter;
