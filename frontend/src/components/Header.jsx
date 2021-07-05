import React, { useEffect, useState, useContext } from "react";
import { Container, Form, FormControl, InputGroup, Nav, Navbar, NavDropdown, Row } from "react-bootstrap";
import { Avatar, notification, message } from "antd";
import { UserOutlined } from "@ant-design/icons";
import { useHistory } from "react-router";

import logo from "../assets/img/logo.svg";
import userApi from "../services/user.js";
import "../style/components/Header.scss";
import { GENRES } from "../utils/constants";
import * as Helpers from "../utils/helpers.js";
import { Messages } from "../utils/messages";

function Header() {
    const [inputSearch, setInputSearch] = useState("");
    const auth = Helpers.getLocalStorage("auth");

    const history = useHistory();

    const handleLogout = async () => {
        try {
            await userApi.logout().then();

            message.success(Messages.logoutSuccess);
            setTimeout(() => {
                Helpers.removeAuth();
                history.push("/");
            }, 200);
        } catch {
            notification["error"]({
                message: Messages.apiErrorMes,
                description: Messages.loginFailed,
            });

            Helpers.removeAuth();
            history.push("/");
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (inputSearch.length > 0) {
            const searchText = inputSearch.trim().replaceAll(" ", "+");
            history.push(`/search/?q=${searchText}`);
        }
    };

    return (
        <div className="header">
            <Container>
                <Row>
                    <Navbar expand="lg">
                        <Navbar.Brand href="/">
                            <img src={logo} style={{ width: "140px", height: "40px" }} alt="" />
                        </Navbar.Brand>
                        <Navbar.Toggle aria-controls="basic-navbar-nav" />
                        <Navbar.Collapse id="basic-navbar-nav">
                            <Nav className="mr-auto">
                                <NavDropdown title="Genres" id="basic-nav-dropdown">
                                    {GENRES.map((genre, index) => {
                                        return (
                                            <NavDropdown.Item href={`/genre/${genre}`} key={index}>
                                                {genre}
                                            </NavDropdown.Item>
                                        );
                                    })}
                                </NavDropdown>
                                <Nav.Link href="/recommend">Recommend</Nav.Link>
                            </Nav>
                            <Form inline onSubmit={handleSubmit}>
                                <InputGroup>
                                    <FormControl
                                        type="text"
                                        placeholder="Search for a movie....."
                                        className="mr-md-4"
                                        onChange={(e) => {
                                            setInputSearch(e.target.value);
                                        }}
                                    />
                                </InputGroup>
                            </Form>
                            {Helpers.isLogin() ? (
                                <Nav>
                                    <NavDropdown
                                        title={
                                            <>
                                                <Avatar size="small" icon={<UserOutlined />} src={auth?.avatar} />
                                                <span style={{ marginLeft: "5px" }}>{auth.username}</span>
                                            </>
                                        }
                                        id="basic-nav-dropdown"
                                        className="dropdown-menu-lg-right"
                                    >
                                        <NavDropdown.Item href={`/u/${auth.username}`}>Profile</NavDropdown.Item>
                                        <NavDropdown.Item onClick={handleLogout}>Logout</NavDropdown.Item>
                                    </NavDropdown>
                                </Nav>
                            ) : (
                                <Nav>
                                    <Nav.Link href="/login">Login</Nav.Link>
                                    <Nav.Link href="/register">Join TMDB</Nav.Link>
                                </Nav>
                            )}
                        </Navbar.Collapse>
                    </Navbar>
                </Row>
            </Container>
        </div>
    );
}

export default Header;
