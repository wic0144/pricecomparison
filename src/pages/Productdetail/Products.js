import React from "react";
import { Row, Col, Button, Card, CardBody, CardTitle, CardText, CardSubtitle, CardImg } from "reactstrap";

import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import uuid from "uuid/v4";
import Widget from "../../components/Widget/Widget";
import s from "./Products.module.scss";

class Products extends React.Component {
  state = {
    options: {
      position: "top-right",
      autoClose: 5000,
      closeOnClick: false,
      pauseOnHover: false,
      draggable: true,
    },
  };

  componentDidMount() {
    toast.success("Thanks for checking out Messenger!", {
      position: "bottom-right",
      autoClose: 5000,
      closeOnClick: true,
      pauseOnHover: false,
      draggable: true,
    });
  }

  addSuccessNotification = () =>
    toast.success(
      "Showing success message was successful!",
      this.state.options
    );

  toggleLocation = (location) => {
    this.setState((prevState) => ({
      options: {
        ...prevState.options,
        position: location,
      },
    }));
  };

  addInfoNotification = () => {
    let id = uuid();
    toast(
      <div>
        Launching thermonuclear war...
        <Button
          onClick={() => this.launchNotification(id)}
          outline
          size="xs"
          className="width-100 mb-xs mr-xs mt-1"
        >
          Cancel launch
        </Button>
      </div>,
      {
        ...this.state.options,
        className: "Toastify__toast--primary",
        toastId: id
      }
    );
  };

  launchNotification = (id) =>
    toast.update(id, {
      ...this.state.options,
      render: "Thermonuclear war averted",
      type: toast.TYPE.SUCCESS,
    });

  addErrorNotification = () => {
    let id = uuid();
    toast.error(
      <div>
        Error destroying alien planet <br />
        <Button
          onClick={() => this.retryNotification(id)}
          outline
          size="xs"
          className="width-100 mb-xs mr-xs mt-1"
        >
          Retry
        </Button>
      </div>,
      { ...this.state.options, toastId: id }
    );
  };

  retryNotification = (id) =>
    toast.update(id, {
      ...this.state.options,
      render: "Alien planet destroyed!",
      type: toast.TYPE.SUCCESS,
    });

  render() {
    return (
      <div className={s.root}>
        <Row>
          <Col
            xs="3"
          >
            <Card
              className={s.ProductCard_productCard}
            >
              <CardBody>
                <CardImg
                  alt="Card image cap"
                  src="https://cf.shopee.co.th/file/df6e5b9bef1b86bc7bb78c04ee6e2163"
                  top
                  className={s.ProductCard_productCardPhoto}
                />
                <CardTitle tag="h5" className={s.ProductCard_productsCardTitle}>
                  Card title
                </CardTitle>
                <CardSubtitle
                  className="mb-2 text-muted"
                  tag="h6"
                >
                  Card subtitle
                </CardSubtitle>
                <CardText>
                  Some quick example text to build on the card title and make up the bulk of the card's content.
                </CardText>
                <CardText className={s.ProductCard_productsCardPrice}>
                  123 ฿
                </CardText>
              </CardBody>
            </Card>
          </Col>
          <Col
            xs="3"
          >
            <Card
              className={s.ProductCard_productCard}
            >
              <CardBody>
                <CardImg
                  alt="Card image cap"
                  src="https://cf.shopee.co.th/file/df6e5b9bef1b86bc7bb78c04ee6e2163"
                  top
                  className={s.ProductCard_productCardPhoto}
                />
                <CardTitle tag="h5" className={s.ProductCard_productsCardTitle}>
                  Card title
                </CardTitle>
                <CardSubtitle
                  className="mb-2 text-muted"
                  tag="h6"
                >
                  Card subtitle
                </CardSubtitle>
                <CardText>
                  Some quick example text to build on the card title and make up the bulk of the card's content.
                </CardText>
                <CardText className={s.ProductCard_productsCardPrice}>
                  123 ฿
                </CardText>
              </CardBody>
            </Card>
          </Col>  <Col
            xs="3"
          >
            <Card
              className={s.ProductCard_productCard}
            >
              <CardBody>
                <CardImg
                  alt="Card image cap"
                  src="https://cf.shopee.co.th/file/df6e5b9bef1b86bc7bb78c04ee6e2163"
                  top
                  className={s.ProductCard_productCardPhoto}
                />
                <CardTitle tag="h5" className={s.ProductCard_productsCardTitle}>
                  Card title
                </CardTitle>
                <CardSubtitle
                  className="mb-2 text-muted"
                  tag="h6"
                >
                  Card subtitle
                </CardSubtitle>
                <CardText>
                  Some quick example text to build on the card title and make up the bulk of the card's content.
                </CardText>
                <CardText className={s.ProductCard_productsCardPrice}>
                  123 ฿
                </CardText>
              </CardBody>
            </Card>
          </Col>  <Col
            xs="3"
          >
            <Card
              className={s.ProductCard_productCard}
            >
              <CardBody>
                <CardImg
                  alt="Card image cap"
                  src="https://cf.shopee.co.th/file/df6e5b9bef1b86bc7bb78c04ee6e2163"
                  top
                  className={s.ProductCard_productCardPhoto}
                />
                <CardTitle tag="h5" className={s.ProductCard_productsCardTitle}>
                  Card title
                </CardTitle>
                <CardSubtitle
                  className="mb-2 text-muted"
                  tag="h6"
                >
                  Card subtitle
                </CardSubtitle>
                <CardText>
                  Some quick example text to build on the card title and make up the bulk of the card's content.
                </CardText>
                <CardText className={s.ProductCard_productsCardPrice}>
                  123 ฿
                </CardText>
              </CardBody>
            </Card>
          </Col>  <Col
            xs="3"
          >
            <Card
              className={s.ProductCard_productCard}
            >
              <CardBody>
                <CardImg
                  alt="Card image cap"
                  src="https://cf.shopee.co.th/file/df6e5b9bef1b86bc7bb78c04ee6e2163"
                  top
                  className={s.ProductCard_productCardPhoto}
                />
                <CardTitle tag="h5" className={s.ProductCard_productsCardTitle}>
                  Card title
                </CardTitle>
                <CardSubtitle
                  className="mb-2 text-muted"
                  tag="h6"
                >
                  Card subtitle
                </CardSubtitle>
                <CardText>
                  Some quick example text to build on the card title and make up the bulk of the card's content.
                </CardText>
                <CardText className={s.ProductCard_productsCardPrice}>
                  123 ฿
                </CardText>
              </CardBody>
            </Card>
          </Col>  <Col
            xs="3"
          >
            <Card
              className={s.ProductCard_productCard}
            >
              <CardBody>
                <CardImg
                  alt="Card image cap"
                  src="https://cf.shopee.co.th/file/df6e5b9bef1b86bc7bb78c04ee6e2163"
                  top
                  className={s.ProductCard_productCardPhoto}
                />
                <CardTitle tag="h5" className={s.ProductCard_productsCardTitle}>
                  Card title
                </CardTitle>
                <CardSubtitle
                  className="mb-2 text-muted"
                  tag="h6"
                >
                  Card subtitle
                </CardSubtitle>
                <CardText>
                  Some quick example text to build on the card title and make up the bulk of the card's content.
                </CardText>
                <CardText className={s.ProductCard_productsCardPrice}>
                  123 ฿
                </CardText>
              </CardBody>
            </Card>
          </Col>  <Col
            xs="3"
          >
            <Card
              className={s.ProductCard_productCard}
            >
              <CardBody>
                <CardImg
                  alt="Card image cap"
                  src="https://cf.shopee.co.th/file/df6e5b9bef1b86bc7bb78c04ee6e2163"
                  top
                  className={s.ProductCard_productCardPhoto}
                />
                <CardTitle tag="h5" className={s.ProductCard_productsCardTitle}>
                  Card title
                </CardTitle>
                <CardSubtitle
                  className="mb-2 text-muted"
                  tag="h6"
                >
                  Card subtitle
                </CardSubtitle>
                <CardText>
                  Some quick example text to build on the card title and make up the bulk of the card's content.
                </CardText>
                <CardText className={s.ProductCard_productsCardPrice}>
                  123 ฿
                </CardText>
              </CardBody>
            </Card>
          </Col>  <Col
            xs="3"
          >
            <Card
              className={s.ProductCard_productCard}
            >
              <CardBody>
                <CardImg
                  alt="Card image cap"
                  src="https://cf.shopee.co.th/file/df6e5b9bef1b86bc7bb78c04ee6e2163"
                  top
                  className={s.ProductCard_productCardPhoto}
                />
                <CardTitle tag="h5" className={s.ProductCard_productsCardTitle}>
                  Card title
                </CardTitle>
                <CardSubtitle
                  className="mb-2 text-muted"
                  tag="h6"
                >
                  Card subtitle
                </CardSubtitle>
                <CardText>
                  Some quick example text to build on the card title and make up the bulk of the card's content.
                </CardText>
                <CardText className={s.ProductCard_productsCardPrice}>
                  123 ฿
                </CardText>
              </CardBody>
            </Card>
          </Col>  <Col
            xs="3"
          >
            <Card
              className={s.ProductCard_productCard}
            >
              <CardBody>
                <CardImg
                  alt="Card image cap"
                  src="https://cf.shopee.co.th/file/df6e5b9bef1b86bc7bb78c04ee6e2163"
                  top
                  className={s.ProductCard_productCardPhoto}
                />
                <CardTitle tag="h5" className={s.ProductCard_productsCardTitle}>
                  Card title
                </CardTitle>
                <CardSubtitle
                  className="mb-2 text-muted"
                  tag="h6"
                >
                  Card subtitle
                </CardSubtitle>
                <CardText>
                  Some quick example text to build on the card title and make up the bulk of the card's content.
                </CardText>
                <CardText className={s.ProductCard_productsCardPrice}>
                  123 ฿
                </CardText>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Products;
