import React from "react";
import { Row, Col, Button, Card, CardBody, CardTitle, CardText, CardSubtitle, CardImg } from "reactstrap";

import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import uuid from "uuid/v4";
import Widget from "../../components/Widget/Widget";
import s from "./Products.module.scss";
import axios from 'axios';

class Products extends React.Component {


  state = {
    options: {
      position: "top-right",
      autoClose: 5000,
      closeOnClick: false,
      pauseOnHover: false,
      draggable: true,
    },
    data: [],
  };

  componentDidMount() {
    const uri = "http://localhost:9200/test/_search?size=100"
    axios.get(uri, { headers: { "content-type": "application/x-www-form-urlencoded", "Accept": "*/*" } })
      .then(res => {
        var data = res.data.hits.hits
        // this.setState({ data: res.data.hits.hits })
        // const test =
        this.setState({ data: data })
        console.log(res.data.hits.hits)
      })
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
        <h1 className="page-title">
          E-commerce -  &nbsp;
          <small>
            <small>Product Grid</small>
          </small>
        </h1>

        <Row>
          {this.state.data.map(data =>
            <Col
              xs="3"
            >
              <Card
                as="a"
                className={s.ProductCard_productCard}
                onClick={data._source.URL}
                style={{ cursor: "pointer" }}
              >
                <CardBody>
                  <CardImg
                    alt="Card image cap"
                    src={data._source.Image}
                    top
                    className={s.ProductCard_productCardPhoto}
                    href={data._source.URL}
                  />
                  <CardTitle tag="h5" className={s.ProductCard_productsCardTitle}>
                    {data._source.Name}
                  </CardTitle>
                  <CardSubtitle
                    className="mb-2 text-muted"
                    tag="h6"
                  >
                    {data._source.Platform}
                  </CardSubtitle>
                  <CardText>

                  </CardText>
                  <CardText className={s.ProductCard_productsCardPrice}>
                    {data._source.Price} ฿
                  </CardText>
                </CardBody>
              </Card>
            </Col>
          )}
        </Row>
      </div>
    );
  }
}

export default Products;
